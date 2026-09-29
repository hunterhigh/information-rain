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

## 仍未决定的正文过渡动画

`text-transition-comparison.html` 对应未决事务 `UT-01`，用于比较节点文字过渡。当前主页面仍使用原有动画；最终选择见[决定 0010](../../../../docs/project/decisions/0010-reading-interaction-refinement.md)。
