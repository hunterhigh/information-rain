# 第二轮五部作品的节点与路径结构复核

状态：来源结构复核｜适用产品：分发产品资料库｜日期：2026-10-08

## 产物和口径

每部作品目录新增 `structure.json`，由[结构脚本](../structure_round_02.py)与[人工判断清单](../data/round-02-structure-decisions.json)生成。它保留源 passage 正文、原始文件路径与标签，并列出选项文案、目标、语法类型、条件待查标记、结局、重玩链接及 `display/include` 依赖。样式、脚本、遥测等列在 `specialPassages`，不作为叙事节点。原始源文件保持不变。

五部合计 **296 个叙事节点、460 条静态选择/跳转、20 个经人工标注的结局**。其中 19 个结局能沿显式文本目标找到静态候选路径；另 1 个受源文件断链影响。候选路径仅说明文字图连通，不证明宏条件、时间或运行时状态允许这条路。路径步骤及选项文案保存在各文件的 `audit.pathStepsToEndings`。

| 作品 | 节点 / 跳转 / 结局 | 起点与代表路径 | 复核结果 |
| --- | ---: | --- | --- |
| [Who Stole My Heart?](../works/hydrohaven--who-stole-my-heart/structure.json) | 33 / 55 / 3 | `IntroductionScreen → PlayerIntro → RamClass1Start → … → LockerStart → LockerHasLetters → EpilogueRam`；另有 Rolex、独处尾声。 | 三个尾声均有静态候选路径。`$ramPoints`、`$rolexPoints` 和“先读信”条件控制实际可选项；全选 Ram/Rolex 正向节点可累计到各自门槛，独处对应低分路径，但未在 Harlowe 运行时逐组合试玩。`SendData` 作为遥测依赖排除。 |
| [Wunderkammer: Plague](../works/kikayang--wunderkammer/structure.json) | 23 / 29 / 1 | `Start → People → Prologue_1 → … → Duty → The End → Epilogue`。 | `The End` 仍通过 `(link:)` 与 `(goto:)` 转入真正尾声；静态目标均存在。延时宏、外部音画及少量状态宏未运行验证。 |
| [Mystery Forest](../works/sannyaa--mystery-forest/structure.json) | 40 / 59 / 9 | `Introduction → Awakening in the Forest → … → Facing the Echo Keeper → …` 可进入离开、守护、森林吞没等不同结果。 | 9 个已标终局均有静态路径；显式链接无断链，也无静态不可达的叙事节点。`A Peaceful Surrender` 返回开头，是循环结果，不计终局。 |
| [I Dont Think of You Anymore](../works/mcaitsmith--i-dont-think-of-you-anymore/structure.json) | 68 / 133 / 1 | `Intro → Intro part 2 → Intro part 3 → … → Focus. → loop → moment.` | `moment.` 是收束；`ending 2–8` 是反复尝试。静态最短路径越过 `$options >= 5` 等门槛，**不能按首轮直接走通**。额外的[条件状态探针](../data/round-02-breakup-state-witness.json)按源码 `if/set` 找到 37 步候选路径：先完成一次失败循环，累积 `$options`，再设置 `$entropy = 1` 后进入收束。`timed` 展示与 180 秒致谢仍未在运行时验证。 |
| [WITHERING_TEARS](../works/hugofmramos--withering-tears/structure.json) | 132 / 184 / 6 | `Disclaimer → TitleScreen → Intro1 → …`；5 个终局有静态路径。 | `Run5 → Run6` 在源文件中断链：目标 passage 实际命名为 `\ Run6`，故 `RunENDING` 不能按原链接到达。`Go to the lake` 也是静态孤立节点。`Shoot her and take the book` 虽带 `ENDING` 标签，正文继续进入 `BADEnding1–5`，不应误判为终局。其余多处状态、音轨和脚本未运行验证。 |

## 需要保留的区别

- `sourceBody` 是可核对的原文，不是已清除 Twine 宏的读者正文；原图可能有动态条件、重玩、自循环和外部资源。结构化数据用于检索、比较与后续编辑，不直接注册到产品内容池。
- `choices[].condition = needs_review` 代表所在 passage 出现控制宏，需要进一步辨认具体选项的显示条件；它不是已判定“不可达”。`static_candidate` 也只说明没有被当前解析器识别到控制宏。
- 结局节点的重玩链接单列为 `replayLinks`，不计故事出口。`audit.staticPathsToEndings` / `pathStepsToEndings` 是以静态图求出的最短候选路径，包含受条件遮蔽的选择。
- 《WITHERING_TEARS》的源断链不在资料原件上修补；若未来转换，应先在工作表中说明是编辑修复还是弃用该结局，再检查读者可见因果。
- 分手循环的条件探针只解释当前文件用到的 `$options`、`$ending`、`$entropy` 简单赋值和 `if/else`；将 `timed` 链接视为延时后可用。`$options` 在 20 封顶，因为源码门槛最高为 20，路径中的 20 表示“至少 20”而非精确点击数。它验证了这组源码条件下存在一条候选路径，不代表 SugarCube 浏览器实际运行、所有状态组合或读者时长。

本次已复核各作起点、代表性分叉、终局定义和静态图异常；没有宣称逐状态组合的完整运行时覆盖。后续若制作内容包，必须按[转换契约](../../../products/distribution/twine-content-conversion.md)另做语义重写、状态决策、逐结局试读与产品注册验收。
