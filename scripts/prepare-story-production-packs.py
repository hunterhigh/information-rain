"""Prepare reviewable reader packs from editable story manuscripts.

Draft output stays under dist/. Release output is refused until each story has
completed editorial review and explicit display metadata, including a measured
reading duration. Registration remains a separate operation.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STORIES = ROOT / "docs/products/distribution/story-production/stories"
CATALOG = ROOT / "docs/products/distribution/story-production/PUBLISH-METADATA.json"
DEFAULT_OUTPUT = ROOT / "dist/story-production-packs"
NODE = re.compile(r"^## ([ne]\d+) · (.+)$", re.MULTILINE)
CHOICE = re.compile(r"^- → ([ne]\d+)：(.+)$", re.MULTILINE)
DIRECTIONS = ("left", "right", "up", "down")


def parse_story(path: Path) -> tuple[str, dict]:
    source = path.read_text(encoding="utf-8")
    title = source.splitlines()[0].removeprefix("# ").strip()
    matches = list(NODE.finditer(source))
    if not title or not matches:
        raise ValueError(f"{path}: missing title or nodes")
    data = {}
    for index, match in enumerate(matches):
        node_id, node_title = match.groups()
        if node_id in data:
            raise ValueError(f"{path}: duplicate {node_id}")
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        raw = source[match.end() : end].strip()
        choices = list(CHOICE.finditer(raw))
        body = CHOICE.sub("", raw).strip()
        if not body:
            raise ValueError(f"{path}: {node_id} has no prose")
        if node_id.startswith("e"):
            if choices:
                raise ValueError(f"{path}: ending {node_id} has choices")
            data[node_id] = {
                "text": body,
                "isEnding": True,
                "title": node_title,
                "summary": body.split("。", 1)[0].strip() + "。",
            }
        else:
            if not 1 <= len(choices) <= 4:
                raise ValueError(f"{path}: {node_id} has {len(choices)} choices")
            data[node_id] = {
                "text": body,
                "exits": {direction: choice.group(1) for direction, choice in zip(DIRECTIONS, choices)},
                "labels": {direction: choice.group(2).strip() for direction, choice in zip(DIRECTIONS, choices)},
            }
    return title, data


def review_blockers(folder: Path) -> list[str]:
    review_path = folder / "REVIEW.md"
    if not review_path.exists():
        return ["missing REVIEW.md"]
    review = review_path.read_text(encoding="utf-8")
    blockers = []
    if not re.search(r"状态：故事就绪", review):
        blockers.append("editorial review has not marked the story ready")
    if "未计时" in review or "未测" in review:
        blockers.append("path reading time remains unmeasured")
    return blockers


def metadata(folder: Path, title: str, data: dict, release: bool, catalog: dict) -> tuple[dict, list[str]]:
    values = catalog["assets"].get(folder.name, {})
    theme = catalog["themes"].get(values.get("themeKey"))
    required = ("author", "desc", "duration", "tags", "theme")
    chosen = {**values, "author": catalog.get("author"), "theme": theme,
              "duration": values.get("duration") or catalog.get("duration")}
    blockers = [f"missing PUBLISH-METADATA.json/{field}" for field in required if not chosen.get(field)]
    if release and blockers:
        return {}, blockers
    first = data["n01"]["text"].split("。", 1)[0].strip()
    return {
        "id": folder.name,
        "image": f"./images/{folder.name}.png",
        "title": title,
        "author": chosen.get("author") or "信息雨（待审署名）",
        "desc": chosen.get("desc") or first + "。",
        "duration": chosen.get("duration") or "待实读计时",
        "tags": chosen.get("tags") or ["分支故事"],
        "theme": chosen.get("theme") or {"bg": "#101820", "accent": "#e3b66b", "particles": "rain"},
        "nodes": sum(not item.get("isEnding", False) for item in data.values()),
        "ends": sum(item.get("isEnding", False) for item in data.values()),
        "startNode": "n01",
        "data": data,
    }, blockers


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--release", action="store_true", help="require every editorial and metadata gate")
    parser.add_argument("--preview", action="store_true", help="prepare an explicitly authorized unreviewed preview")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if args.release and args.preview:
        parser.error("--release and --preview cannot be combined")
    raw_catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    catalog = {
        **raw_catalog,
        "assets": {item["id"]: item for item in raw_catalog["assets"]},
    }
    folders = sorted(path.parent for path in STORIES.glob("*/STORY.md"))
    if set(catalog["assets"]) != {folder.name for folder in folders}:
        raise ValueError("PUBLISH-METADATA.json IDs must match the story directories exactly")
    report = []
    prepared = []
    for folder in folders:
        title, data = parse_story(folder / "STORY.md")
        values, metadata_blockers = metadata(folder, title, data, args.release or args.preview, catalog)
        blockers = review_blockers(folder) + metadata_blockers
        cover = folder / "cover.png"
        if not cover.exists():
            blockers.append("missing cover.png")
        report.append({"id": folder.name, "title": title, "blockers": blockers})
        if values and cover.exists():
            prepared.append((folder, values, cover))
    if args.release and any(item["blockers"] for item in report):
        print(json.dumps({"ready": 0, "blocked": report}, ensure_ascii=False, indent=2))
        return 1
    if args.preview and any(
        any(reason.startswith("missing ") for reason in item["blockers"])
        for item in report
    ):
        print(json.dumps({"preview": 0, "blocked": report}, ensure_ascii=False, indent=2))
        return 1
    output = args.output.resolve()
    dist_root = ROOT / "dist"
    if output == dist_root or dist_root not in output.parents:
        raise ValueError("output must be a subdirectory of this repository's dist directory")
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    for folder, values, cover in prepared:
        package = output / folder.name
        images = package / "images"
        images.mkdir(parents=True)
        (package / "world-entry.js").write_text(
            json.dumps(values, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        shutil.copy2(cover, images / f"{folder.name}.png")
    (output / "preparation-report.json").write_text(
        json.dumps({"mode": "release" if args.release else "preview" if args.preview else "draft", "stories": report}, ensure_ascii=False, indent=2)
        + "\n",
        encoding="utf-8",
    )
    mode = "release" if args.release else "preview" if args.preview else "draft"
    print(f"Prepared {len(prepared)} {mode} packs at {output}")
    print(f"Stories with release blockers: {sum(bool(item['blockers']) for item in report)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
