"""Fetch the approved round-02 Twee snapshots and verify the local corpus.

Usage: python round_02_pipeline.py ingest | verify
Ingest needs authenticated GitHub CLI; verify is offline and uses only stdlib.
"""

from __future__ import annotations

import base64
import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "data" / "round-02-manifest.json"
CATALOG = ROOT / "data" / "catalog.json"
WORKS = ROOT / "works"


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_stats(data: bytes) -> dict:
    content = data.decode("utf-8")
    return {
        "bytes": len(data),
        "sha256": hashlib.sha256(data).hexdigest(),
        "passages": len(re.findall(r"(?m)^::\s*\S", content)),
        "bracket_links": len(re.findall(r"\[\[[^\]]+\]\]", content)),
    }


def fetch(spec: dict, path: str) -> bytes:
    endpoint = (
        f"repos/{spec['repo']}/contents/{quote(path, safe='/')}"
        f"?ref={spec['revision']}"
    )
    result = subprocess.run(
        ["gh", "api", endpoint], capture_output=True, text=True, check=True, timeout=60
    )
    record = json.loads(result.stdout)
    if record.get("encoding") != "base64" or record.get("type") != "file":
        raise ValueError(f"Unexpected GitHub response: {spec['id']} / {path}")
    data = base64.b64decode(record["content"], validate=False)
    git_blob = hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()
    if git_blob != record["sha"]:
        raise ValueError(f"Git blob mismatch: {spec['id']} / {path}")
    return data


def validate_manifest(manifest: dict, catalog: dict) -> None:
    if manifest["round"] != 2:
        raise ValueError("Expected round 2 manifest")
    existing = {work["id"] for work in catalog["works"]}
    seen: set[str] = set()
    for spec in manifest["works"]:
        ident = spec["id"]
        owner = spec["repo"].split("/", 1)[0].lower()
        if not re.fullmatch(r"[a-z0-9-]+--[a-z0-9-]+", ident) or not ident.startswith(owner + "--"):
            raise ValueError(f"Invalid or mismatched ID: {ident}")
        if ident in seen or (ident in existing and not any(w.get("round") == 2 and w["id"] == ident for w in catalog["works"])):
            raise ValueError(f"Duplicate work ID: {ident}")
        if not re.fullmatch(r"[0-9a-f]{40}", spec["revision"]):
            raise ValueError(f"Revision must be a full commit: {ident}")
        if not spec["files"] or len(spec["files"]) != len(set(spec["files"])):
            raise ValueError(f"Missing/duplicate file paths: {ident}")
        for path in spec["files"]:
            parts = Path(path).parts
            if Path(path).is_absolute() or Path(path).drive or ".." in parts or "\\" in path or not path.endswith((".tw", ".twee", ".tws")):
                raise ValueError(f"Unsafe source path: {path}")
        seen.add(ident)


def ingest() -> None:
    manifest, catalog = read_json(MANIFEST), read_json(CATALOG)
    validate_manifest(manifest, catalog)
    timestamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    records = []
    downloads = []
    # Fetch and validate every file before writing, so a network failure cannot
    # leave a partly updated catalog.
    for spec in manifest["works"]:
        files = []
        for path in spec["files"]:
            data = fetch(spec, path)
            stats = source_stats(data)
            if stats["passages"] < 5 or stats["bracket_links"] < 2:
                raise ValueError(f"Unexpectedly sparse source: {spec['id']} / {path}")
            files.append({"path": path, **stats})
            downloads.append((spec["id"], path, data))
        records.append({
            "id": spec["id"], "title": spec["title"], "scope": spec["scope"],
            "round": 2, "retrieved_at_utc": timestamp,
            "source_repository": f"https://github.com/{spec['repo']}",
            "source_commit": spec["revision"], "source_files": files,
        })
    for ident, path, data in downloads:
        target = WORKS / ident / "source" / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    for spec in manifest["works"]:
        (WORKS / spec["id"] / "README.md").write_text(
            f"# {spec['title']}\n\n"
            f"- 范围：{spec['scope']}\n"
            f"- 来源：[{spec['repo']}](https://github.com/{spec['repo']}/tree/{spec['revision']})\n"
            f"- 获取时间：{timestamp}\n"
            f"- 源文件：{len(spec['files'])} 个；原始路径保留在 [source/](source/)；校验值见"
            "[总目录](../../data/catalog.json)。\n\n"
            f"保留依据：{spec['selection_note']}\n\n"
            f"转换提醒：{spec['conversion_note']}\n\n"
            "节点、选项、跳转与结局见[结构数据](structure.json)；其解析范围和限制见"
            "[结构复核](../../notes/2026-10-08-round-02-structure-review.md)。\n\n"
            "详细取舍见[第二轮清洗记录](../../notes/2026-10-08-round-02-screening.md)。\n",
            encoding="utf-8",
        )
    catalog["works"] = [w for w in catalog["works"] if w.get("round") != 2] + records
    write_json(CATALOG, catalog)
    verify()
    print(f"Ingested {len(records)} round-02 works / {len(downloads)} files")


def verify() -> None:
    manifest, catalog = read_json(MANIFEST), read_json(CATALOG)
    validate_manifest(manifest, catalog)
    ids = [work["id"] for work in catalog["works"]]
    if len(ids) != len(set(ids)):
        raise ValueError("Duplicate IDs in catalog")
    by_id = {work["id"]: work for work in catalog["works"]}
    if {s["id"] for s in manifest["works"]} != {w["id"] for w in catalog["works"] if w.get("round") == 2}:
        raise ValueError("Round-02 manifest/catalog membership differs")
    checked = 0
    for spec in manifest["works"]:
        work = by_id[spec["id"]]
        if work["source_commit"] != spec["revision"] or work["source_repository"] != f"https://github.com/{spec['repo']}":
            raise ValueError(f"Source identity mismatch: {spec['id']}")
        if {f["path"] for f in work["source_files"]} != set(spec["files"]):
            raise ValueError(f"File list mismatch: {spec['id']}")
        for item in work["source_files"]:
            path = WORKS / spec["id"] / "source" / item["path"]
            if not path.is_file() or source_stats(path.read_bytes()) != {key: item[key] for key in ("bytes", "sha256", "passages", "bracket_links")}:
                raise ValueError(f"Missing/changed source: {path}")
            checked += 1
    print(f"Verified {len(manifest['works'])} round-02 works / {checked} files")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("ingest", "verify"))
    args = parser.parse_args()
    ingest() if args.command == "ingest" else verify()
