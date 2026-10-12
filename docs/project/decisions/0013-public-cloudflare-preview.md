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

### 2026-09-30 手势快照与滚动修正

- 本次部署地址：[https://9a088148.information-rain-preview.pages.dev/](https://9a088148.information-rain-preview.pages.dev/)
- 部署 ID：`9a088148-3231-496f-a747-c95620979770`
- 对应源码提交：`0b301f2`
- 修正内容：整屏快照保留正文滚动位置；阅读页不再把纵向手势交给系统滚动处理，正文自身仍可滚动。Wrangler 报告部署完成。

### 2026-10-08 手机手势与世界切换修复

- 本次部署地址：[https://debf5c7c.information-rain-preview.pages.dev/](https://debf5c7c.information-rain-preview.pages.dev/)
- 部署 ID：`debf5c7c-1905-48c0-8d95-2d45bf224dc3`
- 对应源码提交：`291b7dd`
- 环境/分支：Production / `main`
- 修正内容：统一清理中断的触摸手势；修复正文与上滑分支导航的手势交接；切换作品时只快照当前封面，并把模糊背景和粒子更新延后到过场结束。
- HTTP 检查：固定部署地址及主地址均返回 200；线上脚本包含本次正文手势交接和快照优化代码。真实手机上的流畅度仍待核验。

### 2026-10-08 `demo-v0.2.0` 发布

- 部署地址：[https://217e2c93.information-rain-preview.pages.dev/](https://217e2c93.information-rain-preview.pages.dev/)
- 部署 ID：`217e2c93-8af6-46e3-aefc-8a282e7f603a`
- 对应 GitHub 版本：`demo-v0.2.0`，提交 `69c6de6`
- 环境/分支：Production / `main`
- 发布内容：手机阅读态由应用接管上下手势；只预加载当前作品及相邻作品封面，减少一次性请求全部封面。
- HTTP 检查：固定部署地址和主域名均返回 200；线上页面包含触摸接管与相邻封面预加载代码。真实手机体验仍待项目所有者核验。

### 2026-10-08 `demo-v0.3.0` 短篇内容预览

- 部署地址：[https://107e70ea.information-rain-preview.pages.dev/](https://107e70ea.information-rain-preview.pages.dev/)
- 主地址：[https://information-rain-preview.pages.dev/](https://information-rain-preview.pages.dev/)
- 部署 ID：`107e70ea-e83f-4a3c-a47c-f2375251b362`
- 对应 GitHub 版本：`demo-v0.3.0`，提交 `b48f5321f520b5a8829598452c8254526e303e89`
- 环境/分支：Production / `main`
- 发布内容：新增 38 篇带封面的短篇分支故事，内容池合计 61 部。署名暂用「信息雨」，体验时长显示「短篇」。项目所有者明确要求直接进入公开预览；完整独立审稿和人类走读计时仍未完成，具体记录见[发布准备记录](../../products/distribution/story-production/DEPLOYMENT-READINESS.md)。
- HTTP 检查：主域名及固定部署地址返回 200；线上注册表下载返回 200，含 61 个作品 ID 和新增作品 `s02-salt-lamp`；固定部署地址上的新封面返回 200。响应仍带 `noindex, nofollow, noarchive`。

### 2026-10-09 `demo-v0.3.1` 封面传输优化

- 固定部署地址：[https://01969c0b.information-rain-preview.pages.dev/](https://01969c0b.information-rain-preview.pages.dev/)
- 部署 ID：`01969c0b-6aa4-4538-9200-dda8d48a45b0`
- 对应 GitHub 版本：`demo-v0.3.1`，提交 `7939508`
- 环境/分支：Production / `main`
- 构建时将 61 张封面转换成舞台 WebP 与缩略图 WebP；原图仍保留在源码内容包。两档发布图合计约 11.4 MiB，原图合计约 107.5 MiB；剧情内容哈希未变。
- HTTP 检查：主页面、运行时目录、新舞台图与缩略图均返回 200；示例 S02 舞台图为 283,820 字节、缩略图为 55,556 字节。设备端加载与滑动性能仍需实测。

### 2026-10-09 `demo-v0.4.0` 双选剧情与纵向作品导航

- 固定部署地址：[https://80abd16e.information-rain-preview.pages.dev/](https://80abd16e.information-rain-preview.pages.dev/)
- 部署 ID：`80abd16e-dcb6-401b-b54f-b3fd2e2481da`
- 对应 GitHub 版本：`demo-v0.4.0`，提交 `1987f1d`
- 环境/分支：Production / `main`
- 61 部作品均满足至少 10 个可达剧情节点与每节点最多两个选项；封面与阅读态统一上滑下一部、下滑上一部。剧情按需载入，页面样式使用本地构建 CSS。
- HTTP 检查：主页面、本地 CSS 与独立剧情 JSON 均返回 200；线上浏览器成功进入首部故事。真实手机触摸体验与独立文学审读仍待验证。

### 2026-10-12 `demo-v0.4.1` 封面纵向滑动修复

- 固定部署地址：[https://011af836.information-rain-preview.pages.dev/](https://011af836.information-rain-preview.pages.dev/)
- 部署 ID：`011af836-05dc-4b89-a288-ea52aed1f539`
- 对应 GitHub 版本：`demo-v0.4.1`，提交 `3e5a3e4`
- 环境/分支：Production / `main`
- 封面氛围图层不再拦截触摸；Swiper 在封面舞台可见后初始化。未改动作品内容，内容 SHA-256 仍为 `2d819d8b47d0d8d980c442feeba33f39900e8a350f4737bbbb286a9a45bab58a`。
- Wrangler 报告部署完成；主域名页面已包含本次两项修复，页面、CSS、内容注册表及抽查的剧情 JSON 返回 200。浏览器控制连接失败，未能实际完成线上拖动；手机真机触摸仍待核验。

## 复核条件

当 Cloudflare Access 权限可用、预览受众扩大、要接入新作品或准备正式发布时，复核本决定；更改访问范围前更新路线图和部署记录。
