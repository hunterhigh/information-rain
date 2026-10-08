# 资料库作品的世界剧情裂变评估

状态：选题审计，尚未制作内容包｜适用产品：分发产品｜日期：2026-10-08

## 范围与计数

本次只评估[资料库](../README.md)现有 **12 部作品、30 个源文件**。其中第二轮 5 部有统一 `structure.json`，首轮 7 部依据原始 `.tw/.twee`、[作品目录](../data/catalog.json)及已有清洗记录阅读。读者[内容池](../../../../products/distribution/reader-web/content-pool/README.md)的 23 个现成包不是裂变输入，也不计入下表。

一个候选“世界剧情”须有可单独说明的处境与戏剧问题、至少两处会改变读者经历或后果的选择，以及回应问题的收束。多个结局若服务于同一问题，仍只计 **一个世界**；章节、单个选项和重复游玩也不单独计数。若原作只有主题或开端，而缺少可借用的选择—后果链，就不计数。这里的“裂变”是提取体验设计供独立创作，不是复制原文或换名上架。

结论：**15 个候选方向**，覆盖 12 部作品；其中 **8 个优先进入独立故事设计，7 个须先补强因果或收束**。这不是 15 个现成内容包，也不是可发布量。第二轮的路径检查只是静态候选路径；首轮未统一生成结构图。选题判断还需经实际编辑试写与逐分支试读验证。

## 候选清单

“优先”表示原作中已有较清楚的冲突、分支后果和结果；“待重构”表示核心值得试，但要补独立背景、有效分支或新的收束。工作标题仅用于区分方向，不是产品标题。

| 编号 | 来源与工作标题 | 可提取的闭环体验及源节点 | 级别 | 成立条件与主要缺口 |
| --- | --- | --- | --- | --- |
| 01 | [Interview Interview](../works/ronynn--interview-interview/README.md)｜聚光灯后的面试 | 用 `interview.tw` 的公众形象问答，经 `cint5` 梦醒，再接 `job.tw` 的现实求职结果：玩家塑造的“理想自我”如何面对真实处境。 | 待重构 | 两章的选择多是人格计分与对话变化；要让前段选择在现实面试中产生可见代价，而非仅靠梦醒反转。 |
| 02 | 同上｜约会中的边界 | 从 `dat.tw` 的约会对话进入 `STALKER_REALIZATION`，到 `DATE_ENDING_THOUGHTS` / `datend`：察觉对方越界后如何回应和退出。 | 待重构 | 原作部分选择汇流；要补互不等价的处理路径和安全、关系层面的结果。此方向与 01 的戏剧问题不同，因此分开计。 |
| 03 | [凌霄錄](../works/jaymoda88--ling-xiao-lu/README.md)｜受伤的妖兽 | `32-vol3.twee` 的 `yaodan_intro → yaodan_win/lose`：急需力量时，是夺取濒死生物的核心，还是冒险救它并建立合作。 | 优先 | 救助与夺取已有不同结果，但依赖战斗和功法状态；须改成可读的选择、代价及局部结局。 |
| 04 | 同上｜被操控的刺客 | `60-vol4.twee` 的 `yinli_ambush → yinli_falter`，接 `61-yinli.twee` 的 `yinli_unbind`，再到 `mingzun_confront → mingzun_win`：识破控制、救回刺客的意志、面对操控者。 | 优先 | 原战斗胜负及回到大地图不能照搬；须让救与不救都能完成短篇收束，并交代刺客自主选择。 |
| 05 | 同上｜最后一道门 | `100-vol6.twee` 的 `truth_reveal → seal_break → ascension_choice` 与四种 `end_*`：得知前世牺牲后，在超越、陪伴、留守与夺权之间定结局。 | 待重构 | 终局依赖六卷人物关系和心魔数值；需新建短篇前史，不能把四个终局直接拼成独立故事。 |
| 06 | [Chinatown Memo](../works/thedavidweng--chinatown-memo/README.md)｜父亲的葬礼 | `1960 → Time to go → Please promise me… → The funeral began → Escape → 2011`：主角能否在丧事商业流程中守住父亲意愿与家族记忆。 | 待重构 | 原作选择多汇流，甚至承诺与实际葬礼发生冲突；须明确不同决定的后果。历史叙述需与虚构机制分开处理。 |
| 07 | [Intergalactic Chat Simulator](../works/ronynn--intergalactic-chat-simulator/README.md)｜把陌生人送到终点 | 旅途中可在 `run` 抛下同伴，也可继续协助其失败的宇宙通信计划，最终经 `Leave this place` 或 `Meet parents` 收束：完成交易还是回应对方和自己的家庭牵挂。 | 优先 | 多数闲聊选项汇流；只保留真正改变互信、任务和结局的节点，修顺原文因果。 |
| 08 | [The Sacrificial Trail](../works/ronynn--the-sacrificial-trail/README.md)｜抵达祭坛之前 | 路线、补给、时间和献祭的连续取舍通往 `Victory` / `GameOver` / `It hurts.`：为避免更大灾祸愿意付出什么。 | 优先 | 时间、资源和累计献祭是体验核心；静态格式需设计有限而清楚的状态等价分支，不能直接删掉系统。 |
| 09 | [Psychotlenij](../works/lapkiteam--psychotlenij/README.md)｜领到设备的代价 | 从 `Начать игру` 的目标，经交通、排队与诊疗荒诞遭遇，到 `Пожаловаться` 根据此前行为进入不同终局：为得到想要的东西，主角如何被制度重新定义。 | 待重构 | 四种结局属于同一个累计评价系统；要先准确核对俄语语义，压缩文化梗与数值。 |
| 10 | [Tarea Final](../works/itruebag94--tarea-final/README.md)｜有限装备的山地求生 | 装备选择接 `DESAFÍO 1–5`，再到 `Pasaje Final` 或失败页：先前准备如何改变雾、火、攀登与风暴中的生存结果。 | 待重构 | 目前较像教学问答；应补人物目标、互斥代价和可感知的选择后果，避免只剩答题。 |
| 11 | [Who Stole My Heart?](../works/hydrohaven--who-stole-my-heart/README.md)｜情人节前的两封信 | 从 `IntroductionScreen` 经过两条同学关系及 `LockerStart/LockerHasLetters`，收束于 `EpilogueRam/Rolex/Alone`：日常互动积累出哪段关系，或选择独处。 | 优先 | 分数门槛和读信条件须转为可见因果；两个恋爱尾声和独处尾声是同一世界的分支，不计三部。 |
| 12 | [Wunderkammer: Plague](../works/kikayang--wunderkammer/README.md)｜疫城里的隐瞒 | `Prologue_2` 的公开、隐藏或秘密准备，接墓地与医生证词，最后至 `The End → Epilogue`：危机中如何查清并处理被掩盖的死者。 | 待重构 | 源作把部分选项导向 `WrongChoice` 后重试，缺真正不同的结果；需把错误选项改成有后果的路径。 |
| 13 | [Mystery Forest](../works/sannyaa--mystery-forest/README.md)｜向森林交出什么 | `Awakening in the Forest` 的探索、物件获取和 `Facing the Echo Keeper` 的献物、解谜、另寻路，导向离开、留下或被森林改变的多种终局。 | 优先 | 9 个尾声共享“与森林达成何种关系”的问题，只计一部；需强化选择前的动机与规则提示。 |
| 14 | [I Dont Think of You Anymore](../works/mcaitsmith--i-dont-think-of-you-anymore/README.md)｜最后一次分手对话 | `Intro` 至反复 `loop/ending 2–8`，最终到 `moment.`：不断改写谈话，直到承认关系无法挽回。 | 优先 | 循环与累计状态是关键体验；`moment.` 的 37 步条件路径仅有源码级证据，改编时需重构成读者能理解的阶段变化。 |
| 15 | [WITHERING_TEARS](../works/hugofmramos--withering-tears/README.md)｜目标是谁 | 从 `Intro1` 的追踪到线索和记忆揭示目标身份，再到 `KillENDING`、`Kiss her` 等结果：执行委托，还是承认与目标的旧关系。 | 优先 | 多个终局属于同一身份疑问；`Run5 → Run6` 断链对应结局暂不借用，自伤与恐怖内容须另作编辑把关。 |

## 不另计的切片

- 《Interview Interview》的健身房测验及《凌霄錄》的战斗胜负页，目前主要是数值/能力关卡或返回大地图，缺独立剧情结果。
- 《Chinatown Memo》的 1923–2011 年代段落互为同一生涯背景；单独的年代转换不等于第二部世界。
- 《Intergalactic Chat Simulator》的多个 `GAME OVER`、《Mystery Forest》的九个尾声、《WITHERING_TEARS》的鸭子彩蛋，均不自动增加世界数。
- 《Wunderkammer: Plague》的墓地询问可为 12 号增加张力，但尚不足以独立成另一个闭环。
- 《I Dont Think of You Anymore》的多轮失败对话是 14 号的递进阶段，不是八个独立故事。

## 下一步使用方式

先为优先的 8 个方向各写一页**独立故事设计卡**：核心问题、读者所知信息、两次以上有效选择、各结局的代价、需要移除的状态依赖。优先试写 03、07、14、15，分别检验伦理抉择、关系旅途、时间循环和身份揭示四种体验是否适配当前阅读器。待重构的 7 个方向先解决表中的缺口，再决定是否进入制作。设计卡通过后，才按[Twine 转换契约](../../../products/distribution/twine-content-conversion.md)制作全新内容包与逐分支试读。

本审计只根据作品文本与现有结构数据评估**叙事供给潜力**，不提供阅读时长、留存率、转化率或 PMF 证据。
