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
- 对应仓库提交：`aee4dd8`
- 发布来源：`products/distribution/reader-web/` 的静态发布包；草稿、来源审查文档与开发脚本没有进入构建输出。

### 2026-09-30 手机端滑动与舞台更新

- 部署地址：[https://acb0e6d5.information-rain-preview.pages.dev/](https://acb0e6d5.information-rain-preview.pages.dev/)
- 部署 ID：`acb0e6d5-fe9f-49a4-800a-d6475fecf0c2`
- 环境/分支：Production / `main`
- 对应仓库提交：`c892929`
- HTTP 检查：返回 200；响应仍包含 `X-Robots-Tag: noindex, nofollow, noarchive`。

### 2026-09-30 手机划动方案比较页

- 统一访问入口：[Cloudflare Pages 主域名上的手机动效比较页](https://information-rain-preview.pages.dev/design/mobile-swipe-motion-comparison.html)
- 本次固定部署地址：[https://93525925.information-rain-preview.pages.dev/](https://93525925.information-rain-preview.pages.dev/)
- 部署 ID：`93525925-6988-4f78-9db7-29d6aa5e41eb`
- 环境/分支：Production / `main`
- 首次比较页发布对应提交：`4ae46d2`
- HTTP 检查：主域名页面返回 200；仍带 `noindex, nofollow, noarchive`。
- 说明：手机和桌面访问的是同一个 Pages 项目与静态 HTML。带哈希的部署域名固定指向某次部署快照；日常访问应使用 `information-rain-preview.pages.dev` 主域名。

#### 手机拖动兼容修复

- 对应提交：`96430ff`
- 部署地址：[https://f98cb302.information-rain-preview.pages.dev/](https://f98cb302.information-rain-preview.pages.dev/)
- 部署 ID：`f98cb302-93f7-4359-8fec-2f1dc7dfcd36`
- 访问路径仍为主域名下 `/design/mobile-swipe-motion-comparison.html`；返回 200，当前脚本包含触屏 Touch Events 和鼠标/触控笔 Pointer Events 两条输入路径。

### 2026-09-30 统一作品内容池

- 本次固定部署地址：[https://44aeed12.information-rain-preview.pages.dev/](https://44aeed12.information-rain-preview.pages.dev/)
- 部署 ID：`44aeed12-daca-43a2-88e1-8543fc3d17eb`
- 环境/分支：Production / `main`
- 对应源码提交：`a028997`
- 页面主地址、生成目录、迁移封面及手机动效比较页均返回 200；响应仍带 `noindex, nofollow, noarchive`。
- 作品源文件与创作草稿未进入静态发布包。内容池结构与迁移核对见[决定 0014](0014-unified-distribution-content-pool.md)。

### 2026-09-30 动效比较页自动播放版本

- 发布范围：五个划动转场 GIF 与自动播放比较页；无需依赖设备触摸/拖动事件。
- 页面入口：[同域名动效比较页](https://information-rain-preview.pages.dev/design/mobile-swipe-motion-comparison.html)
- 本次固定部署地址：[https://6d332fa0.information-rain-preview.pages.dev/](https://6d332fa0.information-rain-preview.pages.dev/)
- 部署 ID：`6d332fa0-9a84-4fd3-864d-6dd3bdda4829`
- 对应仓库提交：`ea735a0`
- GIF 路径：`/design/mobile-swipe-motion-gifs/01-arrow-baseline.gif` 至 `05-direction-glow.gif`。
- Wrangler 已报告部署完成；本机网络未能完成外部 HTTP 探测，故不记录为已验证 HTTP 状态。

### 2026-09-30 整屏滑动与分支选择更新

- 预览主地址：[信息雨 Cloudflare Pages](https://information-rain-preview.pages.dev/)
- 本次部署地址：[https://0cf799e6.information-rain-preview.pages.dev/](https://0cf799e6.information-rain-preview.pages.dev/)
- 部署 ID：`0cf799e6-547d-472c-8003-9ab03107620e`
- 对应源码提交：`dafe0df`
- 发布内容：采用整屏滑动浏览作品；阅读中的左右分支加入跟手提示、保留按钮与分支名，并按选择方向播放整屏转场。Wrangler 报告部署完成。

### 2026-09-30 手机划动问题修订

- 本次部署地址：[https://0cf9ece3.information-rain-preview.pages.dev/](https://0cf9ece3.information-rain-preview.pages.dev/)
- 部署 ID：`0cf9ece3-740f-4f93-9637-f87d00c73c81`
- 对应源码提交：`e076aa8`
- 发布内容：手机端隐藏常驻方向箭头；左右分支显示文字提示；整屏跟随手指，松手后根据方向完成切换；正文滚动与分支手势按边界协调。Wrangler 报告部署完成；真机体验仍待核验。

## 复核条件

当 Cloudflare Access 权限可用、预览受众扩大、要接入新作品或准备正式发布时，复核本决定；更改访问范围前更新路线图和部署记录。
