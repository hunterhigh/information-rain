# Information Rain：项目地图

开工状态：**可以开工，但有已记录的后续事项**

## 我们正在做什么

记录并探索手机原生、推荐即生成、多维信息分发的新娱乐媒介。当前已采纳**工具产品 + 分发产品**的双产品方向；「全梦」是技术愿景名，「信息雨」是信息流方法，文字拓扑 Agent 属于工具产品。[决定 0006](docs/project/decisions/0006-two-products-and-medium-validation.md)是最新产品基线。

要解决的问题：现有讨论分散在对话和实验中，缺少一个能区分已确认判断、候选假设、纠正记录与后续工作的长期项目入口。

## 第一阶段

- 建立本地 Git 仓库
- 用一份 README 汇总当前技术愿景、概念边界、合理性判断、纠正记录与关键未知
- 为后续研究、原型和实现保留可恢复的项目上下文

## 初始阶段未做、现在仍不做

- 面向真实用户的产品代码；round1 已另行授权本地机制 Demo
- 技术栈选型
- 外部服务或模型接入
- 部署或公开发布；私有 GitHub 远端已由[决定 0002](docs/project/decisions/0002-private-github-remote.md)单独授权
- 将尚未验证的愿景写成确定产品规格

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

## 当前实验

按[实验脚手架](docs/project/experiment-scaffold.md)逐个推进候选。[旧 v0.1](experiments/round-01/product-01/demo/README.md)仍是撤回的内部机制样本，见[决定 0005](docs/project/decisions/0005-content-first-demo.md)。当前[分发原型](experiments/round-01/distribution-demo/DEMO-BRIEF.md)已获授权从导入的 30 部中删除指定 11 部，并补全保留 19 部的剧情与分支，见[决定 0007](docs/project/decisions/0007-distribution-content-selection.md)；原始导入的 48 条缺失路径仍记录在来源档案中，不应当作修订版的通过条件。全球公开发布先看[合规初探](docs/research/2026-09-28-distribution-compliance.md)，私有试验不等于授权或产品验收。
