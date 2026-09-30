"""Refresh the selected public Twine source snapshots in this directory.

Uses the Python standard library. GitHub CLI login or GITHUB_TOKEN is optional
but helps with GitHub API rate limits. Never writes authentication details.
"""

from __future__ import annotations

import concurrent.futures
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parent
WORKS = ROOT / "works"
CATALOG = ROOT / "data" / "catalog.json"
EXTENSIONS = {".twee", ".tw", ".tws"}
USER_AGENT = "Information-Rain-source-catalog"

# One entry means one work, even when the author split it into many files.
# These are research references, separate from the reader product content pool.
SPECS = [
    {
        "id": "shrine-sample",
        "title": "Shrine sample",
        "repo": "adaumann/speckit-preset-game-narrative-writing",
        "scope": "sample",
        "prefixes": ["game-narrative-writing/specs/shrine-sample/"],
    },
    {
        "id": "nextrock-episode-1",
        "title": "NextRock, episode 1 and common passages",
        "repo": "cliffhall/NextRock",
        "scope": "episode",
        "prefixes": ["project/common/", "project/episodes/ep1/"],
    },
    *[
        {
            "id": f"game-jam-{slug}",
            "title": title,
            "repo": "ronynn/Game-Jam-Submissions",
            "scope": "source snapshot",
            "files": [path],
        }
        for slug, title, path in [
            ("dawn", "Dawn", "Dawn.twee"),
            ("abate", "Abate, part 1", "abate/part1.tw"),
            ("aesthetics", "Aesthetics", "aesthetics.tw"),
            ("catch", "Catch", "catch.tw"),
            ("igcs", "IGCS", "igcs.twee"),
            ("kev", "Kev", "kev/kev.twee"),
            ("ld50", "LD50", "ld50.twee"),
            ("meritocracy", "Meritocracy", "meritocracy/merit.twee"),
            ("nimble", "Nimble", "nimble.twee"),
            ("sac", "SAC", "sac.tw"),
        ]
    ],
    {
        "id": "chinatown-memo",
        "title": "Chinatown Memo",
        "repo": "thedavidweng/Twine-Immigration-Act",
        "scope": "source snapshot",
        "files": ["Chinatown Memo.twee"],
    },
    {
        "id": "stephen-wong",
        "title": "Stephen Wong",
        "repo": "thedavidweng/Twine-Immigration-Act",
        "scope": "source snapshot",
        "files": ["Stephen Wong.twee"],
    },
    {
        "id": "interview-interview",
        "title": "Interview Interview",
        "repo": "ronynn/interview-interview",
        "scope": "source snapshot",
        "prefixes": [""],
    },
    {
        "id": "old-house-test-story",
        "title": "Old House test story",
        "repo": "sagitrs/sgstory",
        "scope": "test sample",
        "prefixes": ["tests/e2e/old-house/src/"],
    },
    {
        "id": "ethertale",
        "title": "ETHERTALE",
        "repo": "Techy-Nature/ETHERTALE",
        "scope": "source snapshot, including engine passages",
        "prefixes": ["src/"],
    },
    {
        "id": "service-suspended",
        "title": "Service Suspended",
        "repo": "Znboston/service-suspended",
        "scope": "source snapshot",
        "files": ["project-1/src/Service Suspended.twee"],
    },
    {
        "id": "twine-interactive-story",
        "title": "Twine Interactive Story",
        "repo": "itruebag94/twine-interactive-story",
        "scope": "source snapshot",
        "prefixes": [""],
    },
    {
        "id": "principe-de-lyssa",
        "title": "Principe de Lyssa",
        "repo": "QuarkSpin/stories",
        "scope": "draft",
        "prefixes": ["stories/drafts/principe-de-lyssa/"],
    },
    {
        "id": "psychotlenij",
        "title": "Psychotlenij",
        "repo": "lapkiteam/Psychotlenij",
        "scope": "source snapshot",
        "files": ["src/game.twee"],
    },
    {
        "id": "ling-xiao-demo",
        "title": "Ling Xiao Demo",
        "repo": "jaymoda88/Ling-Xiao_Demo",
        "scope": "demo, including system passages",
        "prefixes": [""],
    },
    {
        "id": "research-data-incident",
        "title": "Research Data Incident scenario",
        "repo": "cloudpedagogy/cloudpedagogy-word-twine-renderer",
        "scope": "educational sample",
        "files": ["output/twine/research_data_incident_scenario.twee"],
    },
    {
        "id": "after-the-final-battle",
        "title": "After the Final Battle",
        "repo": "mewzicians/After-the-final-battle-test-build",
        "scope": "test build",
        "files": ["After_the_Final_Battle_v19.twee"],
    },
]


def github_token() -> str | None:
    if os.environ.get("GITHUB_TOKEN"):
        return os.environ["GITHUB_TOKEN"]
    try:
        return subprocess.check_output(
            ["gh", "auth", "token"], text=True, stderr=subprocess.DEVNULL, timeout=10
        ).strip()
    except (OSError, subprocess.SubprocessError):
        return None


TOKEN = github_token()


def get_bytes(url: str, *, api: bool = False) -> bytes:
    headers = {"User-Agent": USER_AGENT}
    if api:
        headers["Accept"] = "application/vnd.github+json"
        if TOKEN:
            headers["Authorization"] = f"Bearer {TOKEN}"
    error: Exception | None = None
    for attempt in range(5):
        try:
            with urlopen(Request(url, headers=headers), timeout=35) as response:
                return response.read()
        except (HTTPError, URLError, TimeoutError, ConnectionError) as exc:
            error = exc
            if isinstance(exc, HTTPError) and exc.code in {400, 401, 404}:
                break
            time.sleep(1 + attempt * 2)
    raise RuntimeError(f"Could not fetch {url}: {error}")


def get_json(url: str) -> dict:
    return json.loads(get_bytes(url, api=True))


def selected(path: str, spec: dict) -> bool:
    if Path(path).suffix.lower() not in EXTENSIONS:
        return False
    return path in spec.get("files", []) or any(
        path.startswith(prefix) for prefix in spec.get("prefixes", [])
    )


def fetch_source(item: tuple[dict, str, str]) -> dict:
    spec, commit, path = item
    repo = spec["repo"]
    raw_url = (
        f"https://raw.githubusercontent.com/{repo}/{commit}/"
        + quote(path, safe="/")
    )
    data = get_bytes(raw_url)
    target = WORKS / spec["id"] / "source" / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    text = data.decode("utf-8", errors="replace")
    return {
        "path": path,
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "passages": len(re.findall(r"(?m)^::\s+", text)),
        "bracket_links": len(re.findall(r"\[\[[^\]]+\]\]", text)),
    }


def main() -> None:
    by_repo: dict[str, list[dict]] = {}
    for spec in SPECS:
        by_repo.setdefault(spec["repo"], []).append(spec)

    work_inputs: list[tuple[dict, str, list[str]]] = []
    for repo, specs in by_repo.items():
        commit_data = get_json(f"https://api.github.com/repos/{repo}/commits/HEAD")
        commit = commit_data["sha"]
        tree_sha = commit_data["commit"]["tree"]["sha"]
        tree = get_json(
            f"https://api.github.com/repos/{repo}/git/trees/{tree_sha}?recursive=1"
        )
        if tree.get("truncated"):
            raise RuntimeError(f"GitHub tree was truncated: {repo}")
        paths = [entry["path"] for entry in tree["tree"] if entry["type"] == "blob"]
        for spec in specs:
            picked = sorted(path for path in paths if selected(path, spec))
            if not picked:
                raise RuntimeError(f"No source files found for {spec['id']}")
            if spec.get("files") and sorted(spec["files"]) != picked:
                raise RuntimeError(f"Expected file list changed for {spec['id']}")
            work_inputs.append((spec, commit, picked))
        print(f"Indexed {repo}", flush=True)

    jobs = [
        (spec, commit, path)
        for spec, commit, paths in work_inputs
        for path in paths
    ]
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        downloaded = list(pool.map(fetch_source, jobs))
    lookup = {(spec["id"], path): item for (spec, _, path), item in zip(jobs, downloaded)}

    catalog = {
        "retrieved_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "method": "GitHub commit tree and public raw files",
        "works": [],
    }
    for spec, commit, paths in work_inputs:
        files = [lookup[(spec["id"], path)] for path in paths]
        record = {
            "id": spec["id"],
            "title": spec["title"],
            "scope": spec["scope"],
            "source_repository": f"https://github.com/{spec['repo']}",
            "source_commit": commit,
            "source_files": files,
        }
        catalog["works"].append(record)
        readme = WORKS / spec["id"] / "README.md"
        readme.write_text(
            f"# {spec['title']}\n\n"
            f"- 范围：{spec['scope']}\n"
            f"- 来源：[{spec['repo']}](https://github.com/{spec['repo']}/tree/{commit})\n"
            f"- 获取时间：{catalog['retrieved_at_utc']}\n"
            f"- 源文件：{len(files)} 个；节点标记：{sum(f['passages'] for f in files)} 个；"
            f"方括号链接标记：{sum(f['bracket_links'] for f in files)} 个。\n\n"
            "原始路径保留在 [source/](source/)；完整文件列表和校验值见"
            " [总目录](../../data/catalog.json)。\n",
            encoding="utf-8",
        )

    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    CATALOG.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    work_index = [
        "# 作品索引",
        "",
        "状态：活动资料索引｜适用产品：分发产品",
        "",
        "每个目录保留一个作品或作品样本的公开源文件快照。"
        "“范围”仅说明当前获得的材料类型，不断言作品完整性。",
        "",
        "| 作品 | 范围 | 源文件数 | 来源 |",
        "| --- | --- | ---: | --- |",
    ]
    for work in catalog["works"]:
        work_index.append(
            f"| [{work['title']}]({work['id']}/README.md) | {work['scope']} | "
            f"{len(work['source_files'])} | "
            f"[原仓库]({work['source_repository']}/tree/{work['source_commit']}) |"
        )
    work_index.extend(["", "完整文件清单与校验值见 [数据目录](../data/catalog.json)。", ""])
    (WORKS / "README.md").write_text(
        "\n".join(work_index), encoding="utf-8"
    )
    print(
        f"Saved {len(catalog['works'])} works and {len(jobs)} source files "
        f"({sum(item['bytes'] for item in downloaded)} bytes).",
        flush=True,
    )


if __name__ == "__main__":
    main()
