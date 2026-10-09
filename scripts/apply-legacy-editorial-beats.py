"""Insert reviewed scene beats into every migrated legacy decision bridge."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "products/distribution/reader-web/content-pool/packs"
BEATS = ROOT / "docs/products/distribution/story-production/LEGACY-BRIDGE-BEATS.json"
NOTE_WORLDS = {"twilight", "aot", "hp", "got"}
DESCRIPTIONS = {
    "lotr": "黑门已塌，你却没有随其他戒灵消散。灰烬里有东西回应你的脚步；向西的守望者、向东的古城和留在魔多的残影，正在等待不同的答案。",
    "er": "凌晨两点，三名病人同时抵达急诊。两位同事接手其余床位；你需要亲自追踪其中一例，直到证据足够交给下一班。",
    "twilight": "福克斯的雨季里，你在图书馆发现爱德华留在《失乐园》里的铅笔字。书该还给谁、那些字能否被别人读见，都比一次约见更难决定。",
    "meta_comic": "第十九页之后原本是你的最后一场戏。你发现格线以外有雨，格线以内却没有；作者、读者和背页的人，都将被你下一次伸手改变。",
}
INTERVIEW_REWRITES = {
    "n12_deliberate": "你看见警员胸前的执法记录仪红灯，后视镜里的人影随你的沉默靠近。你还可以说出完整事实，也可以继续咬住谎言；方向盘已经被你握得发滑。",
    "n13_deliberate": "警员把笔放下，等你把最后一句讲完。后备箱里那人的名字像要从舌根挤出来；你也可以继续否认，或者把这场问询推向无法挽回的一步。",
}


def clean_inworld_prose(text: str, world_id: str) -> str:
    if world_id in NOTE_WORLDS:
        text = re.sub(r"\[[^\]]{0,240}注释：[\s\S]*?\]\s*", "", text)
        text = re.sub(r"\[[^\]]{0,240}背景[^\]]*\]\s*", "", text)
    if world_id == "twilight":
        text = text.replace("cafeteria", "食堂")
    return text


def main() -> None:
    editorial = json.loads(BEATS.read_text(encoding="utf-8"))
    all_bridges = 0
    for world_id, beats in editorial.items():
        path = PACKS / world_id / "world-entry.js"
        world = json.loads(path.read_text(encoding="utf-8"))
        bridge_ids = {key for key in world["data"] if key.endswith("_deliberate")}
        if bridge_ids != set(beats):
            raise ValueError(f"{world_id}: beat mapping does not match story bridge nodes")
        for node_id, beat in beats.items():
            if not beat.endswith(("。", "！", "？")):
                raise ValueError(f"{world_id}/{node_id}: beat needs sentence punctuation")
            node = world["data"][node_id]
            if not node["text"].startswith(beat):
                node["text"] = beat + "\n\n" + node["text"]
            node["labels"] = {**node["labels"]}
            all_bridges += 1
        if world_id in NOTE_WORLDS:
            for node in world["data"].values():
                node["text"] = clean_inworld_prose(node["text"], world_id)
        if world_id == "seventhinterview":
            for node_id, prose in INTERVIEW_REWRITES.items():
                node = world["data"][node_id]
                beat = beats[node_id]
                node["text"] = beat + "\n\n" + prose
        if world_id in DESCRIPTIONS:
            world["desc"] = DESCRIPTIONS[world_id]
        path.write_text(json.dumps(world, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    # The original ferry story has eleven pre-existing scenes and no bridge.
    for world_id in NOTE_WORLDS - set(editorial):
        raise ValueError(f"missing editorial mapping for {world_id}")
    print(f"Applied {all_bridges} specific scene beats across {len(editorial)} legacy worlds")


if __name__ == "__main__":
    main()
