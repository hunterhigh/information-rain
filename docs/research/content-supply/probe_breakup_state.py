"""Bounded source-condition probe for the round-02 breakup loop story.

Recognizes this file's simple SugarCube if/else/set macros. Timed links are
treated as available after their delay. This is a source interpreter, not a
browser run of SugarCube.
"""

from __future__ import annotations

from collections import deque
import json
from pathlib import Path
import re

from structure_round_02 import parse_link


ROOT = Path(__file__).resolve().parent
WORK = ROOT / "works" / "mcaitsmith--i-dont-think-of-you-anymore" / "structure.json"
TOKEN = re.compile(r"(?s)<<\s*(/if|if\s+[^>]+|else|set\s+[^>]+)>>|\[\[([^\]\r\n]+)\]\]")
EXPR = re.compile(r"\$(options|ending|entropy)\s+(gte|is)\s+(\d+)")
SET = re.compile(r"\$(options|ending|entropy)\s+to\s+(?:\$(options)\s*\+\s*)?(\d+)")


def passage_result(body: str, before: tuple[int, int, int]) -> tuple[tuple[int, int, int], list[tuple[str, str]]]:
    state = dict(zip(("options", "ending", "entropy"), before))
    frames: list[tuple[bool, bool]] = []
    active = True
    links = []
    for token in TOKEN.finditer(body):
        macro, bracket = token.groups()
        if bracket is not None:
            if active:
                links.append(parse_link(bracket))
            continue
        if macro.startswith("if "):
            match = EXPR.fullmatch(macro[3:].strip())
            if not match:
                raise ValueError(f"Unsupported condition: {macro}")
            variable, op, number = match.groups()
            outcome = state[variable] >= int(number) if op == "gte" else state[variable] == int(number)
            frames.append((active, outcome))
            active = active and outcome
        elif macro == "else":
            if not frames:
                raise ValueError("Unmatched else")
            parent, previous = frames[-1]
            active = parent and not previous
        elif macro == "/if":
            if not frames:
                raise ValueError("Unmatched /if")
            active = frames.pop()[0]
        elif macro.startswith("set ") and active:
            match = SET.fullmatch(macro[4:].strip())
            if not match:
                raise ValueError(f"Unsupported state update: {macro}")
            variable, operand, number = match.groups()
            state[variable] = (state[operand] if operand else 0) + int(number)
    if frames:
        raise ValueError("Unclosed if")
    return (min(state["options"], 20), state["ending"], state["entropy"]), links


def find_witness() -> dict:
    data = json.loads(WORK.read_text(encoding="utf-8"))
    passages = {passage["name"]: passage for passage in data["passages"]}
    queue = deque([("Intro", (0, 0, 0), [])])
    visited = set()
    while queue:
        name, state, steps = queue.popleft()
        key = name, state
        if key in visited:
            continue
        visited.add(key)
        if name == "moment.":
            return {"method": "bounded_source_condition_probe", "target": name,
                    "timedLinks": "available_after_delay", "optionsCappedAt": 20,
                    "statesVisited": len(visited),
                    "steps": steps, "finalState": dict(zip(("options", "ending", "entropy"), state))}
        after, links = passage_result(passages[name]["sourceBody"], state)
        for label, target in links:
            if target in passages and len(steps) < 100:
                queue.append((target, after, steps + [{"from": name, "label": label, "to": target,
                                                     "stateAfterFrom": dict(zip(("options", "ending", "entropy"), after))}]))
    raise ValueError(f"No state-aware witness found after {len(visited)} states")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", choices=("build", "check"), default="build")
    args = parser.parse_args()
    result = find_witness()
    target = ROOT / "data" / "round-02-breakup-state-witness.json"
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.command == "check":
        if not target.is_file() or target.read_text(encoding="utf-8") != rendered:
            raise ValueError(f"State witness is stale or changed: {target}")
    else:
        target.write_text(rendered, encoding="utf-8")
    print(f"Found {len(result['steps'])}-step state-aware witness after {result['statesVisited']} states")
