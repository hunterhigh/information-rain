# 当前工作基线

状态：活动｜最近核对：2026-10-08

本文件回答“现在以什么为准、正在做什么、下一步是什么”。详细定义和证据仍由各自权威文档保存。

## 当前范围

- **长期方向**：工具产品与分发产品两条线；“全梦”是技术愿景名，“信息雨”是信息流方法。见[决定 0006](decisions/0006-two-products-and-medium-validation.md)。
- **当前唯一实施主线**：分发产品，以现有分发 Demo 为工作基线；工具产品不进入当前执行路线。见[决定 0011](decisions/0011-distribution-product-as-active-roadmap.md)。
- **当前产品目标**：运行 Cloudflare Pages 静态预览，核验当前 Demo 的手机端阅读流程；随后逐步迭代为完整、可上线的分发产品。当前地址是项目所有者接受的临时公开预览，不等于正式产品发布。

## 活动状态

- **有效代码基线**：[`products/distribution/reader-web/`](../../products/distribution/reader-web/)；读者页面、运行时内容池和页面专属资源位于此处。
- **内容来源**：23 部作品统一存于 [`content-pool/packs/`](../../products/distribution/reader-web/content-pool/README.md)；HTML 只读取生成目录，顺序由 `display-order.json` 管理。见[决定 0014](decisions/0014-unified-distribution-content-pool.md)。
- **外部内容资料**：[自供给分发内容资料库](../research/content-supply/README.md)现有两轮共 12 部、30 个 Twine 源文件；第二轮 5 部已生成节点、选项、跳转和结局的来源结构图，并记录静态断链及条件待验路径。它是未来内容生产的参考资料，与当前读者内容池分开；目前没有将这些作品转为产品内容。
- **目录状态**：活动产品源码已从实验目录迁入正式产品边界；当前构建脚本生成根目录 `dist/cloudflare-preview/`，该产物可删除并重建。
- **目录治理依据**：工具 Agent 与分发产品共用一个 Git 仓库，但各有独立源码和文档边界；愿景、商业策划、研究证据及项目治理分别归档。详见[决定 0012](decisions/0012-single-repository-product-boundaries.md)与[项目文档索引](README.md)。
- **当前分发产品代码基线**：目录与文档治理提交 `01236f6`；当前产品版本为 `demo-v0.2.0`，已标记并推送至 GitHub `main`。后续工作基于远端 `main`。
- **当前有效版本记录**：`demo-v0.1.0` 为历史基线；`demo-v0.2.0` 汇总其后的主页、内容池、手机导航等已实施更新，并加入本轮触摸接管与封面预加载优化。
- **当前工作阶段**：阶段 0 文档与仓库边界整理完成；阶段 1 静态预览已发布。手机和桌面统一使用 Cloudflare Pages [主地址](https://information-rain-preview.pages.dev/)；手机动效比较页为[同域名子页面](https://information-rain-preview.pages.dev/design/mobile-swipe-motion-comparison.html)。当前生产部署对应 `69c6de6`（Cloudflare 部署 `217e2c93-8af6-46e3-aefc-8a282e7f603a`），预览地址与访问边界见[决定 0013](decisions/0013-public-cloudflare-preview.md)。项目所有者接受临时公开访问；当前没有 Cloudflare Access 限制。
- **已完成动画调整**：主 Demo 采用“轻微落位”；对比页留档，原位叠化与柔焦叠化是未来备选，逐行显现是历史探索。`UT-01` 已关闭，不属于未决事务；未来若要调整，另建新事项。见[决定 0010](decisions/0010-reading-interaction-refinement.md)。
- **本次阅读体验改动**：节点文字切换、字体大小、舞台尺寸、桌面切换时长和手机手势/舞台适配均已实施；尚待所有者真机体验，当前不安排 Demo 试玩。以后是否试用由产品路线图阶段与所有者决定。
- **手机分支视觉已选定并接入**：左/右/上滑分别选择当前节点分支；下滑整屏进入下一部作品。分支采用“光流牵引”，整张阅读画面跟随手指，不出现拖动文字框。手机正文滚动由应用控制：未到边界时滑动正文，到顶部/底部后下一次相应方向手势才切换世界/分支。上方出口提示显示具体文案。已修复多点触摸清理、正文手势交接和切换世界时的快照绘制；自动检查与线上 HTTP 检查通过，真实手机体验仍待核验。无上方分支时的反馈和返回上一部作品的方式仍待决定。依据见[决定 0015](decisions/0015-full-screen-swipe-and-branch-navigation.md)及[手机滑动方向提示参考](../products/distribution/mobile-swipe-review/README.md)。
- **本轮手机优化**：阅读舞台接管触摸，上划选择上方分支、下划进入下一世界，并仅准备当前与相邻封面。作品节点数据启动时整体加载；23 张封面约 3.9 MB，旧实现会一次性引用全部封面。版本 `demo-v0.2.0` 已推送并部署；线上 HTTP 检查通过，手机真机验收仍待完成。Chrome DevTools 性能 MCP 未配置，因此卡顿的实测来源仍待确认。

## 权威材料阅读顺序

1. [START-HERE 项目地图](../../START-HERE.md)：恢复总体范围与入口。
2. [本工作基线](working-baseline.md)：确认现在有效的版本和工作。
3. [分发产品本体](../products/distribution/ontology.md)：理解产品语言和待确认概念。
4. [分发产品路线图](../products/distribution/roadmap.md)：确认阶段、状态与退出依据。
5. [相关决定](decisions/)与当前产品简报、代码、内容来源：核对具体工作证据。

会议纪要用于说明讨论变化及其缘由，不替代本基线、决定文件或路线图。

## 当前下一步

核验手机端整屏滑动与左右分支在真实设备上的手感和辨识度；随后检查主要阅读流程，并决定是否恢复 Access 受控访问、配置 GitHub Actions 自动部署及演练回退。工具 Agent 保持预留，不进入分发产品的构建与部署。
