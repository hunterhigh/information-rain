# 0013：Cloudflare Pages 临时公开预览

日期：2026-09-30｜状态：已采纳并实施

## 背景

阶段 1 要把当前静态 Demo 部署到 Cloudflare Pages，获得真实线上和手机访问环境。现有 Cloudflare OAuth 凭证有 Pages 写入权限，但没有 Access 管理权限；尚未建立访问策略。Pages 地址因此无法限制为只有项目成员可访问。项目所有者确认当前作品已通过审查，并在部署前明确接受临时公开预览。

## 决定

- 允许当前分发 Demo 以可公开访问的 Cloudflare Pages 地址作临时预览。
- 任何获得地址的人均可访问；`noindex` 响应头只降低搜索引擎收录可能，不构成访问限制。
- 当前部署不代表产品正式发布，也不代表已完成手机端体验验收、产品验证或未来作品的审查。
- 当前项目使用 Wrangler Direct Upload。它不会自动连接 Cloudflare 原生 Git 集成；后续可由 GitHub Actions 部署，并用 Git 提交记录追溯每次上传。
- 如要恢复受控访问，需配置并验证 Cloudflare Access，或另行批准其他访问控制方案；在此之前新增作品需先经审查，且不得把当前预览地址宣传为私密链接。

## 部署记录

- Cloudflare Pages 项目：`information-rain-preview`
- 主地址：[https://information-rain-preview.pages.dev/](https://information-rain-preview.pages.dev/)
- 初始部署地址：[https://0d2e9616.information-rain-preview.pages.dev/](https://0d2e9616.information-rain-preview.pages.dev/)
- 部署 ID：`0d2e9616-e978-4178-acc1-05434af6dafd`
- 环境/分支：Production / `main`
- 对应仓库提交：`c892929`
- 发布来源：`products/distribution/reader-web/` 的静态发布包；草稿、来源审查文档与开发脚本没有进入构建输出。

### 2026-09-30 手机端滑动与舞台更新

- 部署地址：[https://acb0e6d5.information-rain-preview.pages.dev/](https://acb0e6d5.information-rain-preview.pages.dev/)
- 部署 ID：`acb0e6d5-fe9f-49a4-800a-d6475fecf0c2`
- 环境/分支：Production / `main`
- 对应仓库提交：`c892929`
- HTTP 检查：返回 200；响应仍包含 `X-Robots-Tag: noindex, nofollow, noarchive`。

## 复核条件

当 Cloudflare Access 权限可用、预览受众扩大、要接入新作品或准备正式发布时，复核本决定；更改访问范围前更新路线图和部署记录。
