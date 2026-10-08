# Twine 作品第二轮补全与清洗

状态：本轮筛选结论｜适用产品：分发产品｜日期：2026-10-08

## 搜集口径

沿用[首轮口径](2026-09-30-quality-screening.md)：单篇可以入选；必须有可辨认的起点、推进与回应主要处境的结局，内部有影响经历或结果的多节点选择，并有可借鉴的叙事做法。此处的“优质”是编辑初筛，不代表读者留存或 PMF 已获验证。

通过 GitHub Code Search 查询 `.twee` 源文件中的 `StoryTitle`、`StoryData`、`Epilogue`、`The End`、`Ending` 等线索，排除明显测试与示例路径，再逐个读取候选文件的开篇、分支节点和结局。共实读 **18 个候选源文件**，保留 **5 部作品、5 个文件**。检索是定向发现，不是对 GitHub 或互动故事总体的随机抽样。

查询入口：[GitHub Code Search](https://github.com/search?q=extension%3Atwee+%22StoryTitle%22+%22The+End%22&type=code)、[Twine 仓库主题](https://github.com/topics/twine-game)。固定提交、路径和校验值见[第二轮清单](../data/round-02-manifest.json)与[总目录](../data/catalog.json)。Twee 的 passage、`StoryTitle`、`StoryData` 结构以 [Twee 3 规范](https://github.com/iftechfoundation/twine-specs/blob/master/twee-3-specification.md)为解析依据。

## 保留：5 部

| 作品 | 闭环与实际选择 | 转换注意 |
| --- | --- | --- |
| [Who Stole My Heart?](../works/hydrohaven--who-stole-my-heart/README.md) | 入学到情人节的连续选择影响关系；到 Ram、Rolex、独处三个尾声。 | Harlowe 状态与额外遥测脚本需隔离。 |
| [Wunderkammer: Plague](../works/kikayang--wunderkammer/README.md) | 博洛尼亚瘟疫中的公共抉择推进到 `The End` 和 `Epilogue`。 | 图片和延时宏是原作体验的一部分。 |
| [Mystery Forest](../works/sannyaa--mystery-forest/README.md) | 物件、道路和守护者抉择导向离开、留下、失败及循环。 | 循环回起点的路径不应误作未完成。 |
| [I Dont Think of You Anymore](../works/mcaitsmith--i-dont-think-of-you-anymore/README.md) | 分手对话的反复尝试揭开循环，最后进入放手的独立收束节点。 | `timed` 宏和 180 秒致谢等待不能等同留存。 |
| [WITHERING_TEARS](../works/hugofmramos--withering-tears/README.md) | 多段行动和关系选择进入明确标记的悲剧、秘密及主线结局。 | 状态、音轨、脚本及自伤主题需要转换前专项复核。 |

作品的 `source/` 均为固定提交的原始字节，未把宏或外部素材“清洗掉”；清洗是作品级筛选、去重和建立可核验索引。文件中的 `passages` / `bracket_links` 只是语法标记数，不保证所有路径可达。未做完整运行时试玩、逐路径验证或读者测试。

## 未收：13 个候选文件

| 候选 | 原因 |
| --- | --- |
| `NoRaincheck/cinder` 的 `alabaster.twee`、`indigo.twee`、`glass.twee` | 具有完整终局，但该仓库是重构文本；`indigo` 还含 `invented closer ... needs transcript check` 注释。原文与改写边界尚未核实，本轮不混入原作参考库。 |
| `mistydemeo/deadsoul/deadsouls.twee` | 由文学文本改编，当前读取未辨认出明确回应主线的终局。 |
| `jvns/twine-stories` 的 `50ms-request.twee`、`docker-connection.twee` | 技术教学/排障路径，虽有 Epilogue，主要价值是知识讲解而非分支剧情。 |
| `m110/a-night-in-innsmouth/assets/game/game.twee` | 地点与状态驱动的游戏；读取到的 `End of Tracks` 仍自循环，未核实完整主线闭环。 |
| `wbstkr/Cosmic-Quest/src/Cosmic Quest.twee` | 仅 5 个 passage、1 个方括号链接，尾部仍是设想注释。 |
| `thedeadparrot/fic-projects/drift/drift.twee` | 实有 14 个 passage 和结局；属高度依赖《环太平洋》人物背景的粉丝小说，本轮优先保留可独立理解的原创情境。 |
| `cssius111/Moonnight-A-Twine-Narrative-on-Epidemic-and-Time/WNV.twee` | 多章节与隐结局并存，但包含大量自动跳转、嵌入脚本和外部音画，当前未能确认连贯可达的主线闭环。 |
| `JJM152/Queen/src/main.twee` | 标题标注 `v 0.12j`，抽取节点集中在开篇推进，未核实终局。 |
| `Myles94/nexus-inc1/Twine Game/NexusInc.twee` | 信息流权衡模拟，有结束页，但主要是机制教学；不纳入本轮故事优选。 |
| `swangtree/the_moth_effect/project/project.twee` | 仓库提交在本轮未能稳定读取，未进入内容判断。 |

去重以作品为单位；同仓库多文件先判断是否同一作品及版本。以上“未收”仅代表本轮可核查证据和选题口径，不是作品质量的普遍评价。下一轮不应自动重试旧候选并默认入库，须先补足当时的缺失证据。
