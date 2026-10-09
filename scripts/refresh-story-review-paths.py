"""Refresh representative ending routes after a manuscript graph changes."""

from __future__ import annotations

from collections import deque
import importlib.util
from pathlib import Path

_source = Path(__file__).with_name("prepare-story-production-packs.py")
_spec = importlib.util.spec_from_file_location("story_preparation", _source)
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
STORIES = _module.STORIES
parse_story = _module.parse_story


def ending_routes(data: dict) -> list[list[str]]:
    queue = deque([["n01"]])
    visited = {"n01"}
    routes = []
    while queue:
        route = queue.popleft()
        node = route[-1]
        if data[node].get("isEnding"):
            routes.append(route)
            continue
        for target in data[node]["exits"].values():
            if target in visited:
                continue
            visited.add(target)
            queue.append([*route, target])
    return routes


def main() -> None:
    updated = 0
    for folder in sorted(STORIES.iterdir()):
        story = folder / "STORY.md"
        review = folder / "REVIEW.md"
        if not story.exists() or not review.exists():
            continue
        _, data = parse_story(story)
        routes = ending_routes(data)
        if len(routes) != sum(item.get("isEnding", False) for item in data.values()):
            raise ValueError(f"{folder.name}: not every ending is reachable")
        source = review.read_text(encoding="utf-8")
        heading = "## 路径清单" if "## 路径清单" in source else "## 路径与结果"
        start = source.index(heading)
        end = source.index("## 文笔与沉浸审读", start)
        lines = [
            "## 路径清单",
            "",
            "以下是每个结局的一条最短代表路径，并非全部选择组合；独立逐路径审读与实读计时尚未完成。",
            "",
            "| 路径 ID 序列 | 终局 | 实读用时 |",
            "| --- | --- | --- |",
        ]
        for route in routes:
            lines.append(f"| {' → '.join(route)} | {data[route[-1]]['title']} | 未计时 |")
        lines.extend(["", ""])
        source = source[:start] + "\n".join(lines) + source[end:]
        source = source.replace(
            "状态：在写｜图路径已列出，尚需逐路径独立审读。",
            "状态：在写｜当前结构检查通过；代表路径已重算，尚需独立逐路径审读。",
            1,
        )
        if heading == "## 路径与结果":
            source = source.replace(
                "状态：在写｜当前停点：全文与四类结局已写；待独立盲读、逐段修订与实际计时走读",
                "状态：在写｜当前结构检查通过；代表路径已重算，尚需独立逐路径审读。",
                1,
            )
        review.write_text(source, encoding="utf-8")
        updated += 1
    print(f"Updated {updated} review route tables")


if __name__ == "__main__":
    main()
