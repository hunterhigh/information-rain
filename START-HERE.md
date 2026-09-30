# Information Rain：项目地图

开工状态：**可以开工，但有已记录的后续事项**

## 我们正在做什么

记录并探索手机原生、推荐即生成、多维信息分发的新娱乐媒介。当前已采纳**工具产品 + 分发产品**的双产品方向；「全梦」是技术愿景名，「信息雨」是信息流方法，文字拓扑 Agent 属于工具产品。[决定 0006](docs/project/decisions/0006-two-products-and-medium-validation.md)是双产品战略基线。

要解决的问题：现有讨论分散在对话和实验中，缺少一个能区分已确认判断、候选假设、纠正记录与后续工作的长期项目入口。

当前唯一实施主线是**分发产品**：以现有 Demo 为工作基线，逐步形成可上线的完整产品。工具产品仍属于长期方向，但当前不在实施队列。见[决定 0011](docs/project/decisions/0011-distribution-product-as-active-roadmap.md)。

## 当前工作从这里恢复

按以下顺序阅读，避免把愿景、产品定义和实现状态混为一谈：

1. [当前工作基线](docs/project/working-baseline.md)
2. [技术愿景本体](docs/vision/ontology.md)
3. [分发产品业务语言本体](docs/products/distribution/ontology.md)
4. [分发产品实施路线图](docs/products/distribution/roadmap.md)
5. [文档、归档与版本工作规则](docs/project/documentation-workflow.md)

## 市场与产品形态研究（候选判断）

- [产品形态、创作者动机与工具/分发关系](docs/research/2026-09-29-product-form-and-creator-strategy.md)：整理短交互故事与泛内容的边界、创作者上传的交换关系、工具 Agent 候选定位、分发和运营影响。
- [英语市场互动短故事竞品证据](docs/research/2026-09-29-interactive-story-competitive-landscape.md)：按上架产品、可玩网页与预发布宣示分层，比较 AI、视频、竖屏、交互、商业化及证据缺口。

两份研究用于后续产品讨论，不修改当前唯一实施主线，也不表示其中候选功能已获批准。

## 第一阶段

- 建立本地 Git 仓库
- 用一份 README 汇总当前技术愿景、概念边界、合理性判断、纠正记录与关键未知
- 为后续研究、原型和实现保留可恢复的项目上下文

## 起始阶段边界与后续授权

以下清单记录项目最初只建设知识库时的边界，不代表当前目标永远不进入产品实施。后续范围变化须以正式决定和当前路线图为准；现行主线见[决定 0011](docs/project/decisions/0011-distribution-product-as-active-roadmap.md)。

- 初始阶段未做面向真实用户的产品代码；之后已授权本地 Demo，目前目标是逐步将分发产品做成可上线产品。
- 技术栈、外部服务和托管数据方案仍未选定，按分发产品路线图逐步决定。
- 部署和公开发布仍需满足项目阶段门并获得相应授权；私有 GitHub 远端已由[决定 0002](docs/project/decisions/0002-private-github-remote.md)单独授权。
- 尚未验证的技术愿景仍不能直接写成确定产品规格。

## 已启用的工程保护

- 项目范围
- 重要决定记录
- Git 变更历史
- 版本管理
- 阶段门
- 最低自动验证
- 敏感配置保护
- 交接与退出

## 原型边界已核对

- 首个机制 Demo 以手机尺寸为主要交互环境；已在 375px 与 390px 浏览器尺寸走查。
- 当前仍不存储真实用户数据，也不连接付费模型服务；Demo 刷新后进度清空。

## 当前分发产品基线

[分发 Demo](experiments/round-01/distribution-demo/DEMO-BRIEF.md)是当前唯一主动维护版本，内容池包含 19 部内置修订作品和 4 部注册内容包。19 部作品的筛选与修订见[决定 0007](docs/project/decisions/0007-distribution-content-selection.md)；注册格式与四包来源见[决定 0009](docs/project/decisions/0009-distribution-content-registry.md)及[内容池说明](experiments/round-01/distribution-demo/content-pool/README.md)。旧 product-01 已撤回并归档；本轮不启动多个 Demo 的组合测试，历史材料见[归档索引](experiments/archive/README.md)。

现有内容结构和代码检查通过不等于内容试玩、产品验收或上线许可。原始导入的 48 条缺失路径仍在来源档案中，不应当作修订版的通过条件。公开发布还须处理[内容权利与合规](docs/research/2026-09-28-distribution-compliance.md)。完整实施顺序见[分发产品路线图](docs/products/distribution/roadmap.md)。
