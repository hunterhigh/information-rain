# 纵向内容流的加载策略参考

日期：2026-10-09｜范围：信息雨静态预览的封面与剧情加载

## 外部工程证据

- [Meta 对 Facebook 视频内容流的工程说明](https://engineering.fb.com/2024/12/10/video-engineering/inside-facebooks-video-delivery-system/)明确区分初次加载、滚动时补充内容、邻近媒体预取与缓存回退，强调只把当下需要的内容送到界面层。该实现面向视频网络请求；我们的文字内容可以借用“轻目录、按需取正文、有限邻近预取”的原则，不需要照搬视频缓冲。
- [Android Media3 的短视频预加载说明](https://developer.android.com/blog/posts/elevating-media-playback-introducing-preloading-with-media3-part-1)针对纵向动态列表按与当前位置的距离确定预加载优先级，并指出预加载不应与当前播放资源争带宽。
- [Meta Reels 对预取的具体取舍](https://developer.android.com/blog/posts/instagram-and-facebook-deliver-instant-playback-and-boost-user-engagement-with-media3-preload-manager)说明过度预取会增加内存并损害滚动性能，Reels 采用相邻预取；这支持当前作品和邻近作品的小窗口策略。
- [Google 的响应式图片指南](https://web.dev/learn/design/responsive-images)建议按实际显示尺寸提供图片、只优先加载首屏重要图、屏外图片延后加载。本文针对网页图片，直接适用于我们的封面。

## 本地对应问题与决定

`demo-v0.3.0` 的 38 张新 PNG 约 103.7 MiB，平均约 2.9 MiB；此前 23 张 JPEG 合计约 3.8 MiB。运行时目录包含全部 61 部作品的完整剧情，线上文件约 589 KiB，并作为阻塞脚本位于页面头部。原有界面已只为当前和相邻作品准备舞台封面，但大图解码、模糊背景和其他层会放大切换成本。

静态预览先在构建时为每张原图生成舞台 WebP 和小封面 WebP；源码原图不变。主页、搜索和收藏使用小封面，舞台使用压缩图，预取仍局限于当前及相邻作品。随后评估把目录与各篇剧情拆开，避免每次首次加载都解析全部正文。性能结果必须用手机或浏览器轨迹验证，构建体积下降本身不等于流畅度验收。
