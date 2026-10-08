"""Check editable Markdown story graphs without requiring covers or registration."""

from __future__ import annotations

import re
import sys
from collections import deque
from pathlib import Path


ROOT = Path(__file__).parent / "stories"
NODE = re.compile(r"^## ([ne]\d+) · .+$", re.MULTILINE)
CHOICE = re.compile(r"^- → ([ne]\d+)：(.+)$", re.MULTILINE)


def inspect_story(folder: Path) -> list[str]:
    errors: list[str] = []
    source = folder / "STORY.md"
    if not source.exists():
        return ["missing STORY.md"]
    content = source.read_text(encoding="utf-8")
    hits = list(NODE.finditer(content))
    if not hits:
        return ["no story nodes"]
    names = [match.group(1) for match in hits]
    if len(names) != len(set(names)):
        errors.append("duplicate node IDs")
    graph: dict[str, list[str]] = {}
    for index, match in enumerate(hits):
        end = hits[index + 1].start() if index + 1 < len(hits) else len(content)
        body = content[match.end():end]
        targets = [choice.group(1) for choice in CHOICE.finditer(body)]
        name = match.group(1)
        graph[name] = targets
        if name.startswith("n") and not targets:
            errors.append(f"{name}: ordinary node without choices")
        if name.startswith("e") and targets:
            errors.append(f"{name}: ending has choices")
        if len(targets) > 4:
            errors.append(f"{name}: more than four choices")
        if not body.strip().split("- →")[0].strip():
            errors.append(f"{name}: missing prose")
    for name, targets in graph.items():
        for target in targets:
            if target not in graph:
                errors.append(f"{name}: missing target {target}")
    start = "n01"
    if start not in graph:
        errors.append("missing n01 start")
    if not any(name.startswith("e") for name in graph):
        errors.append("no endings")
    if start in graph:
        visited: set[str] = set()
        queue = deque([start])
        while queue:
            current = queue.popleft()
            if current in visited or current not in graph:
                continue
            visited.add(current)
            queue.extend(graph[current])
        for name in graph:
            if name not in visited:
                errors.append(f"{name}: unreachable")
    return errors


def main() -> int:
    folders = sorted(path.parent for path in ROOT.glob("*/STORY.md"))
    failures = 0
    for folder in folders:
        errors = inspect_story(folder)
        result = "OK" if not errors else "; ".join(errors)
        print(f"{folder.name}: {result}")
        failures += bool(errors)
    print(f"checked={len(folders)} failed={failures}")
    return int(bool(failures))


if __name__ == "__main__":
    sys.exit(main())
