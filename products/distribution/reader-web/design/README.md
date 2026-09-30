# 分发 Demo 设计材料索引

本目录保留设计探索、实现预览和交互比较材料，供回溯设计过程。图片是特定时点的静态输出，不自动代表已采纳设计；当前页面的实际效果以同级 `../index.html` 为准。

## 主页封面布局探索

- `home-tab-desktop-a-solid.png`：主页布局候选 A，封面保持完整可见。
- `home-tab-desktop-b-current-cover.png`：主页布局候选 B，以当前封面为主要素材。
- `home-tab-desktop-c-visible-cover-mix.png`：主页布局候选 C，混合完整封面和可见封面片段。
- `home-tab-desktop-A-review.png`、`home-tab-desktop-B-review.png`、`home-tab-desktop-C-review.png`：A/B/C 方案评审图。
- `make-home-feed-previews.py`：生成主页布局预览图的脚本。
- `home-tab-ambient.jpg`：当前 Demo 主页使用的环境背景素材；页面是否使用以 `index.html` 为准。

## 背景视觉探索

- `web-ui-background-color-diffusion.*`：色彩扩散候选，SVG 为源稿，PNG 为预览。
- `web-ui-background-glass-wash.*`、`web-ui-background-glass-wash-v2.*`：玻璃雾化候选及第二版，SVG 为源稿，PNG 为预览。
- `web-ui-background-v15-mid-haze.*`：中景雾化候选。
- `web-ui-fogged-ambient-preview.*`：环境雾化候选。
- `web-ui-soft-charcoal-preview.*`：深色柔和候选。

## 页面实现与参考对照预览

- `web-ui-implementation-preview.png`、`web-ui-implementation-mobile-check.png`：某一实现时点的页面预览与窄屏检查截图。
- `web-ui-reference-aligned-preview.png`、`web-ui-reference-aligned-preview-v2.png`、`web-ui-reference-aligned-mobile-check.png`：对照参考稿调整后的预览与窄屏检查截图。

预览截图不是自动化验收记录，也不能替代当前代码或未来正式产品的运行检查。

## 正文过渡动画档案

`text-transition-comparison.html` 是动画方案档案。主页面当前采用“轻微落位”；“原位叠化”和“柔焦叠化”留作后续备选，“逐行显现”保留为历史探索。方案决定和实施边界见[决定 0010](../../../../docs/project/decisions/0010-reading-interaction-refinement.md)。

## 手机划动与场景转场

`mobile-swipe-motion-comparison.html` 并列展示当前箭头点击基线、Tinder 式倾斜跟手、Reels 式整屏移动、场景视差和方向光提示。样例沿用现有 9:16 阅读画面，可直接拖动；Cloudflare 预览发布后，手机与电脑可从同一 Pages 主域名访问 `/design/mobile-swipe-motion-comparison.html`。它是供项目所有者选择的设计草案，不代表任一候选已被采纳；实现参考和适用边界见[开源项目参考](../../../../docs/research/architecture/2026-09-28-github-project-references.md)。
