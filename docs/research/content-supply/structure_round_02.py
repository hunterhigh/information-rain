"""Build and validate source-level story graphs for the five round-02 works.

The result is research data, not a reader content pack. Only explicit static
targets are resolved; macro state, timing and JavaScript are flagged for review.
"""

from __future__ import annotations

from collections import deque
import html
import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "data" / "round-02-manifest.json"
DECISIONS = ROOT / "data" / "round-02-structure-decisions.json"
WORKS = ROOT / "works"
HEADER = re.compile(r"(?m)^::\s*([^\r\n]+)\r?\n")
BRACKET_LINK = re.compile(r"\[\[([^\]\r\n]+)\]\]")
GOTO = re.compile(r'(?i)(?:\(goto:\s*|<<goto\s+)["\']([^"\']+)["\']')
DISPLAY = re.compile(r'(?i)(?:\(display:\s*|<<include\s+)["\']([^"\']+)["\']')
LINK_GOTO = re.compile(
    r'(?is)\(link:\s*["\']([^"\']+)["\']\)\s*\[(.{0,600}?)\(goto:\s*["\']([^"\']+)["\']\)'
)
CONTROL = re.compile(r"(?i)<<\s*(?:if|elseif|else|set|timed|link|run|script|goto)|\((?:if|else-if|else|set|random|link|live|goto):")
SPECIAL_NAMES = {"StoryTitle", "StoryData", "StoryInit", "StoryCaption", "Story JavaScript", "StoryScript", "SendData"}


def parse_header(raw: str) -> tuple[str, list[str]]:
    header = raw.strip()
    header = re.sub(r"\s+\{.*$", "", header)
    match = re.search(r"\s+\[([^]]*)\]$", header)
    if match:
        return header[: match.start()].strip(), match.group(1).split()
    return header, []


def parse_link(inner: str) -> tuple[str, str]:
    if "->" in inner:
        label, target = inner.split("->", 1)
    elif "<-" in inner:
        target, label = inner.split("<-", 1)
    elif "|" in inner:
        label, target = inner.split("|", 1)
    else:
        label = target = inner
    return html.unescape(label.strip().strip("[]")), html.unescape(target.strip().strip("[]"))


def parse_source(path: Path, source_path: str) -> list[dict]:
    content = path.read_text(encoding="utf-8-sig")
    headers = list(HEADER.finditer(content))
    passages = []
    for index, match in enumerate(headers):
        name, tags = parse_header(match.group(1))
        body = content[match.end(): headers[index + 1].start() if index + 1 < len(headers) else len(content)].strip()
        passages.append({"name": name, "tags": tags, "sourceFile": source_path, "body": body})
    return passages


def choices_for(body: str) -> list[dict]:
    edges = []
    for match in BRACKET_LINK.finditer(body):
        label, target = parse_link(match.group(1))
        edges.append({"label": label, "target": target, "syntax": "bracket", "condition": "needs_review" if CONTROL.search(body) else "static_candidate"})
    for match in LINK_GOTO.finditer(body):
        edges.append({"label": match.group(1), "target": match.group(3), "syntax": "harlowe_link_goto", "condition": "needs_review"})
    for match in GOTO.finditer(body):
        target = match.group(1)
        if target not in {item["target"] for item in edges if item["syntax"] == "harlowe_link_goto"}:
            edges.append({"label": None, "target": target, "syntax": "goto_transition", "condition": "needs_review"})
    return edges


def shortest_path(start: str, target: str, adjacency: dict[str, list[str]]) -> list[str] | None:
    queue = deque([(start, [start])])
    seen = {start}
    while queue:
        current, path = queue.popleft()
        if current == target:
            return path
        for next_name in adjacency.get(current, []):
            if next_name not in seen and next_name in adjacency:
                seen.add(next_name)
                queue.append((next_name, path + [next_name]))
    return None


def build_work(spec: dict, decision: dict) -> dict:
    original = []
    for source_path in spec["files"]:
        path = WORKS / spec["id"] / "source" / source_path
        original.extend(parse_source(path, source_path))
    names = [passage["name"] for passage in original]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        raise ValueError(f"Duplicate passage names in {spec['id']}: {duplicates}")
    by_name = {passage["name"]: passage for passage in original}
    if decision["start"] not in by_name or decision["narrativeStart"] not in by_name:
        raise ValueError(f"Missing reviewed start: {spec['id']}")
    if not set(decision["endings"]) <= by_name.keys():
        raise ValueError(f"Missing reviewed endings: {spec['id']}")
    story_data = by_name.get("StoryData", {}).get("body", "")
    try:
        metadata = json.loads(story_data)
    except json.JSONDecodeError:
        metadata = {}
    special = []
    passages = []
    excluded = set(decision["excludeFromNarrativeGraph"])
    for source in original:
        name, body, tags = source["name"], source["body"], source["tags"]
        if name in SPECIAL_NAMES or name.startswith(("StoryStylesheet", "StoryFormat")) or name == "hal.tracks" or "stylesheet" in tags or "script" in tags or name in excluded:
            special.append({"name": name, "tags": tags, "sourceFile": source["sourceFile"], "reason": "excluded_by_review" if name in excluded else "non_narrative"})
            continue
        links = choices_for(body)
        for edge in links:
            edge["resolution"] = "external" if re.match(r"(?i)https?://", edge["target"]) else "resolved" if edge["target"] in by_name else "missing"
        is_ending = name in decision["endings"]
        passage = {
            "name": name, "tags": tags, "sourceFile": source["sourceFile"],
            "sourceBody": body, "choices": [] if is_ending else links,
            "replayLinks": links if is_ending else [],
            "ending": is_ending,
            "hasRuntimeControl": bool(CONTROL.search(body)),
            "includes": DISPLAY.findall(body),
        }
        passages.append(passage)
    story_names = {p["name"] for p in passages}
    adjacency = {p["name"]: [e["target"] for e in p["choices"] if e["resolution"] == "resolved" and e["target"] in story_names] for p in passages}
    paths = {name: shortest_path(decision["start"], name, adjacency) for name in decision["endings"]}
    by_story_name = {p["name"]: p for p in passages}
    path_steps = {}
    for ending, path in paths.items():
        if path is None:
            path_steps[ending] = None
            continue
        steps = []
        for current, next_name in zip(path, path[1:]):
            edge = next(e for e in by_story_name[current]["choices"] if e["target"] == next_name)
            steps.append({"from": current, "label": edge["label"], "to": next_name, "condition": edge["condition"]})
        path_steps[ending] = steps
    reachable = {name for name in adjacency if shortest_path(decision["start"], name, adjacency)}
    missing = sorted({f"{p['name']} → {e['target']}" for p in passages for e in p["choices"] if e["resolution"] == "missing"})
    terminal = sorted(p["name"] for p in passages if not adjacency[p["name"]] and not p["ending"])
    unresolved = sorted(p["name"] for p in passages if p["hasRuntimeControl"] or p["includes"])
    return {
        "schemaVersion": 1, "sourceWorkId": spec["id"], "sourceCommit": spec["revision"],
        "storyFormat": metadata.get("format"), "declaredStart": metadata.get("start"),
        "reviewedStart": decision["start"], "narrativeStart": decision["narrativeStart"],
        "reviewNote": decision["note"], "specialPassages": special,
        "passages": passages,
        "audit": {"narrativePassages": len(passages), "specialPassages": len(special),
                  "staticEdges": sum(len(p["choices"]) for p in passages),
                  "reviewedEndings": decision["endings"], "staticPathsToEndings": paths,
                  "pathStepsToEndings": path_steps,
                  "unreachableByStaticLinks": sorted(story_names - reachable),
                  "nonEndingDeadEnds": terminal, "missingTargets": missing,
                  "runtimeControlPassages": unresolved},
    }


def write_all(*, check: bool = False) -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    decisions = json.loads(DECISIONS.read_text(encoding="utf-8"))["works"]
    if {w["id"] for w in manifest["works"]} != set(decisions):
        raise ValueError("Manifest and structure decisions differ")
    for spec in manifest["works"]:
        result = build_work(spec, decisions[spec["id"]])
        target = WORKS / spec["id"] / "structure.json"
        rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        if check:
            if not target.is_file() or target.read_text(encoding="utf-8") != rendered:
                raise ValueError(f"Structure file is stale or changed: {target}")
        else:
            target.write_text(rendered, encoding="utf-8")
        audit = result["audit"]
        print(f"{spec['id']}: {audit['narrativePassages']} passages, {audit['staticEdges']} edges, "
              f"{len(audit['reviewedEndings'])} endings, {len(audit['missingTargets'])} missing, "
              f"{len(audit['unreachableByStaticLinks'])} static-unreachable")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", nargs="?", choices=("build", "check"), default="build")
    args = parser.parse_args()
    write_all(check=args.command == "check")
