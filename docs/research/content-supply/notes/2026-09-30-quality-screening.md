# Twine 作品清洗与重审记录

状态：本轮筛选结论｜日期：2026-09-30｜对象：首批 24 个作品或样本

## 修订的保留口径

前一轮误将“多章”作为硬条件，漏掉完整的单篇互动故事。本轮撤销该条件，按以下项目判断：

1. **剧情闭环**：能辨认起点、推进和至少一个回应核心情境的结局。单篇可以入选；只有序章、待续、游戏菜单或孤立失败页不够。
2. **真实选择**：作品内部有多个可到达的故事节点，读者选择会改变事件、过程或结局。只有连续“下一步”或纯问答流程不足以作为分支故事参考。
3. **叙事参考价值**：人物、处境、选择代价或结构中至少有值得借鉴的具体做法；同一故事的重复版本只留一份。此项是编辑判断，不等同读者留存表现。

本轮核对了源文件的起点、节点选择、代表性路径、结局及“未完待续”标记；对状态宏复杂的作品仍需在转换前做完整路径与运行时审查。

## 保留：7 部，25 个源文件

| 作品 | 闭环与选择的证据 | 注意事项 |
| --- | --- | --- |
| [Interview Interview](../works/ronynn--interview-interview/README.md) | Chapter 0–4 的主题推进；最终 `scales8` 通向 `The End`，中途有多处面试选择。 | 原仓库独立的 `stat.tw` 统计演示已移出。 |
| [凌霄錄](../works/jaymoda88--ling-xiao-lu/README.md) | 第一至六卷；飞升抉择通往同行、独行、留在人间、堕道等主线结局。 | 仅留 15 个故事文件；原游戏的系统依赖已移出，不能独立运行。 |
| [Chinatown Memo](../works/thedavidweng--chinatown-memo/README.md) | 从 1923 年到 2011 年的家族与社区记忆，多个情境选择最终收束到 `The End`。 | 与同仓库 `Stephen Wong.twee` 的正文近乎相同；只留这一份。 |
| [Intergalactic Chat Simulator](../works/ronynn--intergalactic-chat-simulator/README.md) | 同行、交谈与行动选择导向至少五个标记结局，包括“Meet parents”的主结局。 | 投稿文本有未打磨之处；保留其对话分支与多结局结构作参考。 |
| [The Sacrificial Trail](../works/ronynn--the-sacrificial-trail/README.md) | 逃亡和献祭目标贯穿路线选择，`Victory` 与 `GameOver` 及收束页给出结果。 | 强依赖时间、资源和状态机制；不能直接扁平化成静态选项。 |
| [Psychotlenij](../works/lapkiteam--psychotlenij/README.md) | 俄语讽刺冒险有连续场景、实际选项与四个标记为“концовка”的结局。 | 后续结构研究需要俄语阅读能力；少量源文本含待办注释。 |
| [Tarea Final](../works/itruebag94--tarea-final/README.md) | 比利牛斯山求生从入营、挑战推进到成功到达或不同失败结局；选择影响积分、生命及结果。 | Harlowe 变量与条件结果需逐条核对。 |

保留的是**可参考的故事资料**，并非宣称这些作品已完成逐路径试玩、自动转换或市场验证。

## 移出：17 个作品或样本

| 首批 ID | 本轮理由 |
| --- | --- |
| `after-the-final-battle` | 主体在 JavaScript 引擎中；文本 passage 大多是容器，当前快照未提供可核实的完整故事闭环。 |
| `stephen-wong` | 与保留的 `chinatown-memo` 几乎同一正文，仅标题和部分图片链接不同；去重。 |
| `ethertale` | 游戏引擎和片段内容混合，当前快照未核实完整主线结局。 |
| `game-jam-abate` | 文件标为 `part1`，缺后续收束。 |
| `game-jam-aesthetics` | 虽有多个结局，主要文本与情境衔接仍较粗糙，未达到本轮编辑参考门槛。 |
| `game-jam-catch` | 某结局直接标注 `story incomplete`。 |
| `game-jam-dawn` | `Epilogue` 明确标注 `End of prologue`。 |
| `game-jam-kev` | 有多结局，但严重依赖粉丝梗，文本和选择后果打磨不足；本轮不保留。 |
| `game-jam-ld50` | 周次模拟流程，缺少可辨认的完整叙事收束。 |
| `game-jam-meritocracy` | 以观点问答和辩论为主，`The End` 也写明并非真实结局；故事闭环不清。 |
| `game-jam-nimble` | 多个结局可见，但情节、语气和文字质量不稳定；本轮不作为优质故事参考。 |
| `nextrock-episode-1` | 只有 Episode 1 和通用地点节点，缺主线终局。 |
| `old-house-test-story` | 用于测试的简短故事骨架。 |
| `principe-de-lyssa` | 源文件位于 draft，只有开篇段落。 |
| `research-data-incident` | 教学情境决策材料，有结果但主要是培训流程，并非本轮要收的故事作品。 |
| `service-suspended` | 尾段明确标注 `TO BE CONTINUED...`，核心时间循环尚未收束。 |
| `shrine-sample` | 写作工具样本，非完整独立故事。 |

保留作品内另移出《凌霄錄》的框架、地点、系统及界面文件共 42 个，以及 `Interview Interview` 的独立统计演示 `stat.tw`。这些文件在此前 Git 版本中可追溯；当前活动资料目录与固定版本刷新脚本只收本轮入选文件。

## 统一 ID：旧目录 → 新目录

目录和 `catalog.json` 的 `id` 使用 `<来源 GitHub owner>--<标题短名>`；完整规则见[资料区说明](../README.md)。来源 owner 不是作者字段。

| 首批目录 | 当前目录 |
| --- | --- |
| `interview-interview` | `ronynn--interview-interview` |
| `ling-xiao-demo` | `jaymoda88--ling-xiao-lu` |
| `chinatown-memo` | `thedavidweng--chinatown-memo` |
| `game-jam-igcs` | `ronynn--intergalactic-chat-simulator` |
| `game-jam-sac` | `ronynn--the-sacrificial-trail` |
| `psychotlenij` | `lapkiteam--psychotlenij` |
| `twine-interactive-story` | `itruebag94--tarea-final` |
