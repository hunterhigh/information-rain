# GitHub 开源项目参考：信息雨与文字拓扑 Agent

日期：2026-09-28
状态：研究备忘；Swiper 与 XState 已获项目所有者同意并接入本轮 HTML Demo，其余项目仍是候选方向

## 目的

保存本轮针对信息雨分发产品、文字拓扑 Agent、推荐即生成及媒介升级所做的 GitHub 调研，供以后进入相应阶段时复用。当前项目仍以本地静态 Demo 验证内容与交互。项目所有者已同意把 Swiper 与 XState 用于本轮分发 Demo 的交互试验；这不等于确定正式产品技术栈，其余候选也不会因为本记录自动成为依赖或外部服务。

本轮最直接的产品判断是：不需要寻找一个包办全部能力的框架。更适合的长期分层是：

1. 内容与分支语义；
2. 可达路径和图谱检查；
3. 确定性的阅读与切换状态；
4. 创作者编辑界面；
5. 独立的推荐、生成、评测和媒介生产层。

## 本轮采用方向

### 2026-09-30：阅读态手势反馈候选

阅读态下一步需要讨论的不只是能否识别滑动，还包括“拖动时画面怎么回应、松手后如何确认已进入新段”。参考实现显示有四种值得比较的反馈：

| 参考 | 可借用的交互细节 | 对信息雨的适用边界 |
|---|---|---|
| [Swiper Cards / Creative Effect](https://swiperjs.com/swiper-api) | 跟手位移、卡片堆叠、可调的前后层变换；目前项目已接入 Swiper。 | 可借鉴封面间的位移与落位；正文有可滚动文字和多方向分支，不能把所有手势都交给同一条滑轨。 |
| [react-tinder-card](https://github.com/3DJakob/react-tinder-card) | MIT 许可；位置/速度阈值、未达阈值时回弹、阈值满足时的方向状态提示。 | 上游面向 React；当前是单文件 HTML，因此借鉴手势反馈模型，不为样例迁移框架。 |
| [Motion drag](https://motion.dev/docs/react-drag) | 方向锁定、弹性边界、惯性与拖动中视觉状态。 | 有价值的是手势反馈原则；当前项目可先用现有 Swiper 和 CSS transforms，不必额外加 React 依赖。 |
| [GSAP Draggable](https://gsap.com/docs/v3/Plugins/Draggable/) | 触摸/鼠标统一拖动、边界、速度跟随和抛掷惯性。 | 适合复杂时间轴或更复杂的空间动画；目前可能超出一个阅读舞台的需要。 |

当前交互比较页 [`mobile-swipe-motion-comparison.html`](../../../products/distribution/reader-web/design/mobile-swipe-motion-comparison.html) 将这些模式翻译为当前产品的五个可操作样例：箭头基线、倾斜跟手、整屏跟手、场景视差、方向光提示。它们是讨论材料，不是已批准的产品设计。判断上优先保留正文可读性和分支方向反馈；最终选择前不改主 Demo 的移动端交互。

### 2026-09-30：复用滑动引擎的边界复核

当前手机交互直接复用已集成的 Swiper v14.2.0，没有增加第二套滑动依赖。Swiper 负责封面之间的跟手竖向切换；阅读正文仍由原有页面状态和触摸事件负责，因为正文既要保留自然滚动，也要把横向/边缘竖向动作映射为剧情分支或作品切换。

此前参考的 PeerTube `videos-list.component.ts` 主要处理视频列表、分页和列表状态，不是手势识别或滑动动画引擎，因此不适合复制到当前交互。借用其中与当前目标匹配的列表架构，不意味着需要照搬其 Angular 组件。

依据：[Swiper 官方仓库](https://github.com/nolimits4web/swiper)、[Swiper API](https://swiperjs.com/swiper-api)、[PeerTube 视频列表组件](https://github.com/Chocobozzz/PeerTube/blob/develop/client/src/app/shared/shared-video-miniature/videos-list.component.ts)。开源实现用途的区分是结合源码和当前产品边界作出的工程判断。

### 1. Swiper：已用于本轮分发 Demo 的作品切换试验

- 仓库：[nolimits4web/swiper](https://github.com/nolimits4web/swiper)
- 许可：MIT
- 已确认能力：移动端 1:1 跟手触摸、硬件加速切换、纵向模式、鼠标滚轮、键盘、虚拟幻灯片、懒加载和无障碍支持。
- 截至本次核对，最新发布页显示 v14.2.0；v14 面向较新的浏览器基线。若要兼容较旧设备，应先核对 v12，而不是默认追最新版本。

对当前 Demo 的价值：现有作品切换使用手工 `touchstart`/`touchend` 阈值和两段定时动画。手指移动期间页面不跟随，松手后又经历约 1.1 秒的锁定，造成“越滑越慢”和输入被吞掉的感受。Swiper 可以接管作品封面之间的物理拖动、速度判断、回弹和索引切换。

本轮实际边界：

- Swiper 只负责作品之间的纵向切换，不负责作品内部的剧情方向选择。
- 正文滚动、方向按钮、收藏、搜索与记录页继续由现有界面负责。
- 不把纵向正文滚动与作品切换放进同一个无条件手势区域；只有正文到达边缘或明确退出阅读模式后才允许切换作品。
- 先使用普通 slides；19 部内容不需要立即启用 virtual slides。
- 固定具体版本，不使用不带版本号的 CDN 地址。

当前固定为 v14.2.0，切换动画先取 280ms，并开启跟手拖动、短滑识别、阻尼与边缘释放。已在 375px、390px 浏览器手机视图和桌面视图完成回归；真机触感仍需项目所有者试玩后判断。

### 2. XState：已用于替换散落的布尔锁和隐式状态

- 仓库：[statelyai/xstate](https://github.com/statelyai/xstate)
- 许可：MIT
- 已确认能力：基于事件的状态机、层级状态、并行状态和 actor；运行时零依赖。
- 官方文档当前推荐 v5；发布流中已有 v6 alpha 信息。本轮如试验，应固定稳定的 v5，不采用 alpha。

对当前 Demo 的价值：页面目前同时依赖 `wheelLocked`、`isExploring`、`isAnimating`、计时器、DOM class 和 `currentPage` 判断。它们可能形成互相矛盾的组合，例如视觉动画结束了但锁仍未解除，或切换作品时打字动画仍在运行。

本轮以 v5.33.2 接入，状态机只表达产品语义：

```text
worlds.cover.ready
worlds.cover.switching
worlds.reading.typing
worlds.reading.ready
worlds.reading.transitioning
worlds.reading.ending
search
bookmarks
footprints
profile
```

输入事件可包括 `WORLD_CHANGED`、`ENTER_WORLD`、`TYPE_DONE`、`CHOOSE_DIRECTION`、`EXIT_WORLD` 和 `OPEN_PAGE`。像素位移、触摸速度和回弹仍交给 Swiper；XState 不应复制滑动库的底层工作。

## XState 与 Swiper 的组合边界

```text
触摸 / 滚轮
      ↓
Swiper：拖动、速度、回弹、作品索引
      ↓ WORLD_CHANGED
XState：封面 / 阅读 / 打字 / 结局 / 其他页面
      ↓
现有渲染函数：装载作品、显示节点、更新按钮与记录
```

两者不能同时拥有“切换是否完成”的最终判断。建议由 Swiper 产生索引与过渡完成事件，XState 接收事件并更新语义状态；删除原有固定 500ms + 600ms 的双层锁，而不是在其外面再包一层状态机。

## 本轮 HTML 试验的验收条件

自动检查与浏览器实走已经覆盖内容未变、9:16 画幅、封面切换、进入阅读、打字完成、方向选择和降级路径；以下仍作为项目所有者真机试玩时的完整验收清单：

1. 手指移动时作品画面同步移动；轻滑可以取消，快速滑动可以自然完成。
2. 不再存在固定约 1.1 秒的不可输入窗口；连续滑动不会无提示丢失。
3. 阅读正文时，正常上下滚动不会误切到下一部作品。
4. 封面、阅读、节点打字、方向选择、结局和退出状态之间不存在非法组合。
5. 鼠标滚轮、触摸、键盘和按钮仍有一致结果。
6. 在 375px、390px 手机视图和桌面视图完成实走；同时尊重 `prefers-reduced-motion`。
7. 不改变本轮保留作品的文字、分支或结局；交互改造和内容重构分开验证。
8. CDN 加载失败时有可理解的降级或至少明确失败，不出现空白页面。

## 接入成本与回退

- 直接 CDN 接入虽然适合单文件试验，但增加网络可用性和供应链风险，也与当前“离线体验未验证”的状态叠加。
- 如果试验成立，再决定是否引入构建步骤或保存经许可的固定版本资产；不要从一次 Demo 试验推导正式架构。
- 在接入前保留当前交互实现的 Git 基线。试验失败时应能单独撤回 Swiper/XState 改动，不撤回同期的内容修订。
- 本轮接入基于已完成的 19 部内容修订，不改变作品文字、分支、结局与封面；内容 SHA-256 仍为 `98eff35162a3551505424b167e047a5a94e0900fea85aee6d84b864c8e99ac31`。

## 其他高价值仓库

### 内容语义与文字拓扑 Agent

| 项目 | 已确认用途 | 对项目的推断 | 采用时机 |
|---|---|---|---|
| [inkle/ink](https://github.com/inkle/ink) | 分支叙事语言，支持变量、条件、汇合和后果 | 适合作为内容模型参考，把故事语义与分发 UI 分开 | 设计文字拓扑内容格式时 |
| [y-lohse/inkjs](https://github.com/y-lohse/inkjs) | Ink 的 JavaScript 编译器与运行时 | 如果 Web 端直接运行 Ink，这是首要候选 | Ink 语义验证成立后 |
| [xyflow/xyflow](https://github.com/xyflow/xyflow) | React Flow/Svelte Flow 节点编辑界面 | 适合作为文字拓扑 Agent 的可视化作者界面 | 开始构建工具产品时 |
| [retejs/rete](https://github.com/retejs/rete) | 可视化编程和数据/控制流执行 | 当节点不只表示内容，还执行生成、审核、发布流程时可能比 XYFlow 更合适 | 工具产品需要可执行工作流时 |
| [graphology/graphology](https://github.com/graphology/graphology) | JavaScript/TypeScript 图数据结构与算法 | 可用于不可达节点、孤点、循环、结局和路径深度检查 | 可先用于现有内容审计 |

### 推荐与反馈

| 项目 | 已确认用途 | 对项目的推断 | 采用时机 |
|---|---|---|---|
| [gorse-io/gorse](https://github.com/gorse-io/gorse) | 开源推荐服务，支持多种推荐方法和多模态表示 | 可作为长期推荐服务边界参考，但当前样本量不足 | 有真实行为数据以后 |
| [metarank/metarank](https://github.com/metarank/metarank) | 个性化学习排序和反馈事件 | 其曝光、互动、反馈事件模型值得先借鉴 | 定义产品埋点时先参考，模型后置 |
| [recommenders-team/recommenders](https://github.com/recommenders-team/recommenders) | 推荐系统实践、模型与评测笔记 | 更适合作为知识库，不是产品依赖 | 研究和基准设计阶段 |
| [benfred/implicit](https://github.com/benfred/implicit) | 基于隐式反馈的 ALS、BPR 和相似项模型 | 只有拥有足量阅读、选择、退出信号后才有价值 | 推荐数据成熟后 |

### AI 生成、观测与评测

| 项目 | 已确认用途 | 对项目的推断 | 采用时机 |
|---|---|---|---|
| [vercel/ai](https://github.com/vercel/ai) | TypeScript 模型调用、流式输出、结构化数据和工具调用 | 适合作为“推荐触发结构化生成”的应用层接口 | 首次接入真实模型时 |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | 提示词、Agent、RAG 评测与红队测试 | 可检查连续性、结构、重复、安全和提示注入 | 生成链路开始时同步引入 |
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | LLM tracing、提示词、数据集、实验与评测 | 适合观察生成质量、费用和延迟；静态 Demo 阶段过重 | 出现持续模型调用后 |
| [statelyai/agent](https://github.com/statelyai/agent) | 由状态机限制 LLM 只能选择合法事件 | 思路与信息雨的“模型提出、系统判定是否合法”高度相关，但项目仍在 alpha | 只作架构研究，暂不依赖 |

### 插画、视频与播放器

| 项目 | 已确认用途 | 对项目的推断 | 采用时机 |
|---|---|---|---|
| [Comfy-Org/ComfyUI](https://github.com/Comfy-Org/ComfyUI) | 节点式图像、视频、音频和 3D 生成工作流 | 可把人物、场景和风格约束固化为可重复生成流程 | 插画验证阶段 |
| [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | 用 React 程序化制作和批量渲染视频 | 可把文字、插画、字幕、转场和配音组合成短视频 | 短视频验证阶段；先复核商业许可 |
| [videojs/video.js](https://github.com/videojs/video.js) | 成熟 HTML5 播放器与插件生态 | 适合一般视频分发 | 短视频 Demo 需要播放器时 |
| [shaka-project/shaka-player](https://github.com/shaka-project/shaka-player) | HLS/DASH、自适应流与离线播放 | 当前过重；适合正式流媒体阶段 | 有专业流媒体需求时 |

### 本地体验、实验与诊断

| 项目 | 已确认用途 | 对项目的推断 | 采用时机 |
|---|---|---|---|
| [dexie/Dexie.js](https://github.com/dexie/Dexie.js) | IndexedDB 封装和浏览器本地数据 | 可保存阅读进度、足迹、收藏和离线内容 | 需要持久化本地试用数据时 |
| [GoogleChrome/workbox](https://github.com/GoogleChrome/workbox) | Service Worker 和 PWA 离线缓存 | 可改善弱网与离线体验 | 离线需求被验证后 |
| [rrweb-io/rrweb](https://github.com/rrweb-io/rrweb) | 记录与回放网页交互 | 可观察误滑、停顿和返回；必须先做隐私遮罩 | 有正式体验测试方案时 |
| [growthbook/growthbook](https://github.com/growthbook/growthbook) | 功能开关、A/B 实验和产品分析 | 可验证不同切换速度、提示方式和入口，但不能替代产品判断 | 真实用户与指标定义完成后 |
| [PostHog/posthog](https://github.com/PostHog/posthog) | 产品分析、会话回放、实验和错误追踪 | 能力完整但运维面较大 | 进入真实用户阶段再比较 |
| [automerge/automerge](https://github.com/automerge/automerge) | 本地优先 CRDT 和并发合并 | 只有文字拓扑工具进入多人协作时才值得承担复杂度 | 多人协作需求被验证后 |

## 推荐研究顺序

1. 当前 Demo：Swiper、XState、Graphology。
2. 工具产品内容模型：Ink/inkjs、XYFlow；若节点需要执行流程，再比较 Rete。
3. 真实生成链路：AI SDK、Promptfoo，随后才是 Langfuse。
4. 真实用户与足量事件：Metarank/Gorse、GrowthBook 或产品分析平台。
5. 媒介升级：ComfyUI、Remotion、Video.js/Shaka Player。

## 来源与证据说明

- 事实性能力、许可和发布状态来自各项目官方 GitHub 仓库、发布页或官方文档，核对日期为 2026-09-28。
- “对信息雨的价值”“采用时机”和组合方式属于基于当前项目边界的产品/工程判断，不是上游项目给出的结论。
- Star 数会变化，不能作为采用决定的主要依据，因此本记录不把它当作优先级标准。
- 正式采用前仍应重新核对最新版本、浏览器支持、许可证、安全公告和维护状态。
