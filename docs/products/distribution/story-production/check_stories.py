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
        if len(targets) > 2 and "--strict" in sys.argv:
            errors.append(f"{name}: more than two choices")
        elif len(targets) > 4:
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
        stack: list[tuple[str, tuple[str, ...], int]] = [(start, (), 0)]
        completed = 0
        while stack:
            current, seen, decision_count = stack.pop()
            if current in seen:
                errors.append(f"{current}: cycle in a static story path")
                continue
            if current not in graph:
                continue
            if current.startswith("e"):
                completed += 1
                if decision_count < 2:
                    errors.append(f"{current}: path has fewer than two decisions")
                continue
            if len(seen) > len(graph):
                errors.append("path exceeds graph size")
                break
            for target in graph[current]:
                stack.append((target, seen + (current,), decision_count + int(len(graph[current]) > 1)))
        if completed == 0:
            errors.append("no complete path")
    if "--strict" in sys.argv and sum(name.startswith("n") for name in graph) < 10:
        errors.append("fewer than ten ordinary nodes")
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
