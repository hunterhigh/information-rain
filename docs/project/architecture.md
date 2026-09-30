# 项目初始架构记录

状态：历史决定｜适用范围：Information Rain 项目起始阶段，不代表当前产品部署方案

## 起点记录

项目最初只建立文档型研究仓库，当时的分类为：

- 产品类型：`mobile`
- 运行方式：`local`
- 技术适配器：`docs-only`
- 部署画像：`none`
- 风险等级：`low`

这记录了项目初始阶段“先保存技术愿景和协作基线”的选择，不是当前系统应维持不变的要求。

## 后续边界

2026-09-28 的[决定 0006](decisions/0006-two-products-and-medium-validation.md)将工具 Agent 与分发产品确认为两条独立产品线。当前分发产品已进入实施，读者网页在[`products/distribution/reader-web/`](../../products/distribution/reader-web/)，静态预览方向与阶段状态以[分发产品路线图](../products/distribution/roadmap.md)为准。工具 Agent 的实现仍未开始。

本文件不决定两产品未来的服务端、账号、数据存储或代码共享方式；这些问题应按产品需求逐步设计并记录新决定。
