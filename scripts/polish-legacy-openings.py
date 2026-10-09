"""Apply a small, explicit line edit to each original reader opening.

The edits sharpen the first scene after the binary graph migration. They are
kept as keyed editorial decisions so an editor can compare each line with its
story instead of hiding prose generation inside the migration algorithm.
"""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKS = ROOT / "products/distribution/reader-web/content-pool/packs"
OPENING_LINES = {
    "apocalypse": "门外又敲了一下，这次金属正好碰在你掌心贴着的那块门板上。",
    "garden": "她用拇指压住亮起的屏幕，像怕你先看见那上面的时间。",
    "building": "电梯门合拢前，你看见楼层键里根本没有十四。",
    "midnight": "老板把空碗扣在桌上，那个穿雨衣的人却忽然把椅子往你这边挪了半寸。",
    "neon": "芯片在衣内袋发烫，你想起母亲上一次报出自己名字时，系统里仍查无此人。",
    "wuxia": "信封背面还有一道湿指印，与你握剑的手指恰好对得上。",
    "space": "你把日期重新数了一遍，数字没有错，错的是整艘船的位置。",
    "abyss": "舱壁传来三下轻叩，间隔与母舰约定的报平安信号一模一样。",
    "western": "替你系马的人已经不见，只剩缰绳上一个刚打好的活结。",
    "campus": "锁门的钥匙在你掌心硌出一道红痕，B302 的灯却比走廊的每一盏都亮。",
    "loop": "第七次，你把那二十三分钟写在手背上，笔画还没干，路口已经有人开始过街。",
    "dream": "镜中的你先于你眨了一下眼，掌柜伸手盖住了镜面。",
    "lotr": "晨光刚越过黑门，你的甲片里便响起一声极轻的裂纹。",
    "twilight": "你把那本没人借走的书翻到扉页，纸角上有一道像被指甲反复压过的折痕。",
    "meta_comic": "那枚页码又淡了一层，你数不清还剩几笔墨能留住它。",
    "er": "分诊护士将三张记录倒扣在白板下，最上面一张的时间刚被改过。",
    "aot": "你勒住马，瓦斯罐的重量向左一沉，前方的烟雾信号断在林线后。",
    "hp": "帽檐从你额前移开时，长桌尽头有人把一只正在发亮的魔杖藏进了袖子。",
    "got": "城墙上的号角停了第一声，第二声迟迟没有来，守夜人已经望向同一处雪线。",
    "ashduel": "久濑玄把剑尖移开一寸，露出石庭上昨夜才刻下的第一个名字。",
    "lastferry": "小满把铁盒往怀里压紧，盒盖里有什么东西被水打得轻轻响。",
    "seventhinterview": "巡警的手电照进车里时，后座那道人影比你更早低下了头。",
    "whitehour": "你抬手按住墙面，掌下传来一阵比心跳慢半拍的轻震。",
}

INLINE_NOTE_IDS = {"twilight", "aot", "hp", "got"}


def main() -> None:
    for world_id, line in OPENING_LINES.items():
        path = PACKS / world_id / "world-entry.js"
        world = json.loads(path.read_text(encoding="utf-8"))
        node = world["data"][world["startNode"]]
        text = node["text"]
        if world_id in INLINE_NOTE_IDS:
            text = re.sub(r"^\[[^\]]+\]\s*", "", text, count=1)
        if line not in text:
            text = text.rstrip() + "\n\n" + line
        node["text"] = text
        path.write_text(json.dumps(world, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"polished {world_id}")


if __name__ == "__main__":
    main()
