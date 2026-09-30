"""Restore the curated public Twine source snapshots at fixed commits.

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
        "id": "ronynn--interview-interview",
        "title": "Interview Interview",
        "repo": "ronynn/interview-interview",
        "revision": "2f076256da096a4a2148bb79ee12d1a4267c7f54",
        "scope": "complete five-chapter story",
        "files": ["dat.tw", "gym.tw", "interview.tw", "job.tw", "reptile.tw"],
        "selection_note": "目录列有 Chapter 0–4；最终段落 scales8 标记 The End。",
    },
    {
        "id": "jaymoda88--ling-xiao-lu",
        "title": "凌霄錄",
        "repo": "jaymoda88/Ling-Xiao_Demo",
        "revision": "ad301daf02c839193f3065fd96637a11d563b2e3",
        "scope": "six-volume story passages only",
        "prefixes": ["凌霄錄/src/story/"],
        "selection_note": "src/story/ 包含第一至六卷与第六卷多种结局；这里只保留故事段落，不是可独立运行的游戏源码。",
    },
    {
        "id": "thedavidweng--chinatown-memo",
        "title": "Chinatown Memo",
        "repo": "thedavidweng/Twine-Immigration-Act",
        "revision": "b7365f9ef8f32aa7bbf049a9ee1c873dd33cfea4",
        "scope": "complete historical story",
        "files": ["Chinatown Memo.twee"],
        "selection_note": "1923 至 2011 的家族与社区记忆主线，经多处选择到 The End；同仓库另一标题版本基本重复。",
    },
    {
        "id": "ronynn--intergalactic-chat-simulator",
        "title": "Intergalactic Chat Simulator",
        "repo": "ronynn/Game-Jam-Submissions",
        "revision": "0eaadbfdaf3997e8fe759182893687aac73b1098",
        "scope": "complete branching story",
        "files": ["igcs.twee"],
        "selection_note": "从日常出发，经同行和对话选择抵达多个有差异的标记结局。",
    },
    {
        "id": "ronynn--the-sacrificial-trail",
        "title": "The Sacrificial Trail",
        "repo": "ronynn/Game-Jam-Submissions",
        "revision": "0eaadbfdaf3997e8fe759182893687aac73b1098",
        "scope": "complete narrative game",
        "files": ["sac.tw"],
        "selection_note": "逃亡与献祭主线有阶段选择及 Victory、GameOver、TheEnd 收束；状态规则需要人工理解。",
    },
    {
        "id": "lapkiteam--psychotlenij",
        "title": "Psychotlenij",
        "repo": "lapkiteam/Psychotlenij",
        "revision": "b5d79319a966bba9c0f8860b0c59f13ec0428c41",
        "scope": "complete satirical story",
        "files": ["src/game.twee"],
        "selection_note": "俄语讽刺冒险有连续场景、实际选项与四个明确标记的结局。",
    },
    {
        "id": "itruebag94--tarea-final",
        "title": "Tarea Final",
        "repo": "itruebag94/twine-interactive-story",
        "revision": "8ef57e0acf0e31290e42cd87acedef3c8c51bb44",
        "scope": "complete survival story",
        "files": ["Tarea Final_IgnacioTruebaGandur.twee"],
        "selection_note": "西语比利牛斯山求生故事包含五项挑战、分支失败结局与到达终点的结局。",
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
        owner = spec["repo"].split("/", 1)[0].lower()
        if not re.fullmatch(r"[a-z0-9-]+--[a-z0-9-]+", spec["id"]):
            raise RuntimeError(f"Invalid work ID: {spec['id']}")
        if spec["id"].split("--", 1)[0] != owner:
            raise RuntimeError(f"Work ID owner does not match source: {spec['id']}")
        by_repo.setdefault(spec["repo"], []).append(spec)

    work_inputs: list[tuple[dict, str, list[str]]] = []
    for repo, specs in by_repo.items():
        revision = specs[0]["revision"]
        if any(spec["revision"] != revision for spec in specs):
            raise RuntimeError(f"Conflicting revisions for {repo}")
        commit_data = get_json(f"https://api.github.com/repos/{repo}/commits/{revision}")
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
            " [总目录](../../data/catalog.json)。\n\n"
            f"本轮筛选保留依据：{spec['selection_note']}"
            "细节见[清洗记录](../../notes/2026-09-30-quality-screening.md)。\n",
            encoding="utf-8",
        )

    CATALOG.parent.mkdir(parents=True, exist_ok=True)
    CATALOG.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    work_index = [
        "# 作品索引",
        "",
        "状态：活动资料索引｜适用产品：分发产品｜筛选日期：2026-09-30",
        "",
        "当前保留剧情有收束、内部有实际选择且可供叙事结构参考的完整作品；单篇也可入选。"
        "筛选依据和移出清单见[清洗记录](../notes/2026-09-30-quality-screening.md)。",
        "",
        "| 作品 | 保留依据 | 源文件数 | 来源 |",
        "| --- | --- | ---: | --- |",
    ]
    for work in catalog["works"]:
        selection_note = next(spec["selection_note"] for spec in SPECS if spec["id"] == work["id"])
        work_index.append(
            f"| [{work['title']}]({work['id']}/README.md) | {selection_note} | "
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
