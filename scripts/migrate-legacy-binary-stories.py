"""One-time structural migration of the original 23 reader worlds.

Each three-way scene becomes two consecutive binary decisions. The existing
scene's prose is split at a paragraph (or sentence) boundary, so the second
decision presents authored story context instead of an empty menu. No ending
or original route is removed. The migration is deterministic and idempotent.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "products/distribution/reader-web/content-pool/packs"
LEGACY_IDS = """apocalypse garden building midnight neon wuxia space abyss western
campus loop dream lotr twilight meta_comic er aot hp got ashduel lastferry
seventhinterview whitehour""".split()
ORDER = ("left", "right", "up", "down")


def divide_prose(text: str) -> tuple[str, str]:
    paragraphs = [item.strip() for item in re.split(r"\n\s*\n", text.strip()) if item.strip()]
    if len(paragraphs) >= 2:
        cut = len(paragraphs) // 2
        return "\n\n".join(paragraphs[:cut]), "\n\n".join(paragraphs[cut:])
    sentences = re.findall(r"[^。！？!?]+[。！？!?]?", text.strip())
    sentences = [item for item in sentences if item.strip()]
    if len(sentences) >= 2:
        cut = max(1, len(sentences) // 2)
        return "".join(sentences[:cut]).strip(), "".join(sentences[cut:]).strip()
    commas = list(re.finditer(r"[，,；;]", text))
    if commas:
        cut = commas[len(commas) // 2].end()
        return text[:cut].strip(), text[cut:].strip()
    return text.strip(), "眼前的两条路都还开着，你得在下一步作出决定。"


def migrate(world: dict) -> tuple[dict, int, int]:
    data = world["data"]
    added = 0
    remapped = 0
    for node_id, node in list(data.items()):
        if node.get("isEnding"):
            continue
        exits = node.get("exits", {})
        labels = node.get("labels", {})
        directions = [direction for direction in ORDER if direction in exits]
        if len(directions) == 3:
            bridge_id = f"{node_id}_deliberate"
            if bridge_id in data:
                raise ValueError(f"{world['id']}/{bridge_id}: bridge ID collision")
            first, second = divide_prose(node["text"])
            if not first or not second:
                raise ValueError(f"{world['id']}/{node_id}: cannot split prose")
            first_dir, second_dir, third_dir = directions
            data[bridge_id] = {
                "text": second,
                "exits": {"left": exits[second_dir], "right": exits[third_dir]},
                "labels": {"left": labels[second_dir], "right": labels[third_dir]},
            }
            node["text"] = first
            node["exits"] = {"left": exits[first_dir], "right": bridge_id}
            node["labels"] = {"left": labels[first_dir], "right": "再看另一条路"}
            added += 1
        elif directions != ["left", "right"]:
            if len(directions) > 2:
                raise ValueError(f"{world['id']}/{node_id}: more than three choices")
            node["exits"] = {side: exits[direction] for side, direction in zip(("left", "right"), directions)}
            node["labels"] = {side: labels[direction] for side, direction in zip(("left", "right"), directions)}
            remapped += 1
    world["nodes"] = sum(not node.get("isEnding", False) for node in data.values())
    if world["nodes"] < 10:
        raise ValueError(f"{world['id']}: fewer than ten story nodes")
    return world, added, remapped


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="rewrite the 23 legacy pack files")
    args = parser.parse_args()
    total_added = total_remapped = 0
    for world_id in LEGACY_IDS:
        path = PACKS / world_id / "world-entry.js"
        world = json.loads(path.read_text(encoding="utf-8"))
        if world["id"] != world_id:
            raise ValueError(f"{path}: ID mismatch")
        world, added, remapped = migrate(world)
        total_added += added
        total_remapped += remapped
        print(f"{world_id}: {world['nodes']} scenes; {added} decisions split; {remapped} directions remapped")
        if args.apply and (added or remapped):
            path.write_text(json.dumps(world, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"total: {total_added} new scenes; {total_remapped} direction changes; apply={args.apply}")


if __name__ == "__main__":
    main()
