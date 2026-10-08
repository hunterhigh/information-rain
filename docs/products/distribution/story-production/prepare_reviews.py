"""Create path inventories for story reviews without claiming editorial approval."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).parent / "stories"
HEADING = re.compile(r"^## ([ne]\d+) · (.+)$", re.MULTILINE)
CHOICE = re.compile(r"^- → ([ne]\d+)：(.+)$", re.MULTILINE)


def make_review(story: Path) -> str:
    source = story.read_text(encoding="utf-8")
    matches = list(HEADING.finditer(source))
    nodes: dict[str, tuple[str, list[tuple[str, str]]]] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source)
        nodes[match.group(1)] = (
            match.group(2),
            CHOICE.findall(source[match.end() : end]),
        )

    rows: list[str] = []

    def visit(node: str, route: list[str], choices: list[str]) -> None:
        if node in route:
            rows.append(f"| {' → '.join(route + [node])} | 循环，需人工检查 | 未计时 |")
            return
        title, exits = nodes[node]
        path = route + [node]
        if node.startswith("e"):
            rows.append(f"| {' → '.join(path)} | {title} | 未计时 |")
            return
        for target, label in exits:
            visit(target, path, choices + [label])

    visit("n01", [], [])
    title = source.splitlines()[0].removeprefix("# ")
    return (
        f"# {title}｜审稿记录\n\n"
        "状态：在写｜图路径已列出，尚需逐路径独立审读。\n\n"
        "## 路径清单\n\n"
        "| 路径 ID 序列 | 终局 | 实读用时 |\n"
        "| --- | --- | --- |\n"
        + "\n".join(rows)
        + "\n\n## 文笔与沉浸审读\n\n"
        "- 开篇盲读：待记录。\n"
        "- 整路朗读与结局差异：待记录。\n"
        "- 逐段牵引与防御性写作：待记录。\n"
        "- 来源差异化与文风卡兑现：待记录。\n\n"
        "## 下一动作\n\n"
        "按上表逐路审读、修稿、记录真实用时；图检查通过后再判定故事就绪。\n"
    )


def main() -> None:
    created = 0
    for story in sorted(ROOT.glob("*/STORY.md")):
        review = story.with_name("REVIEW.md")
        if review.exists():
            continue
        review.write_text(make_review(story), encoding="utf-8")
        created += 1
    print(f"review scaffolds created={created}")


if __name__ == "__main__":
    main()
