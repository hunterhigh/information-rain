# 分发产品源码

**状态：当前实施主线。** 产品定义、业务术语和路线图由 [`docs/products/distribution/`](../../docs/products/distribution/) 维护。

| 位置 | 职责 |
| --- | --- |
| [`reader-web/`](reader-web/) | 当前读者网页、运行时注册表、作品包、封面和页面专属设计资源；构成一个独立的静态部署单元。 |
| [`reader-web/content-pool/`](reader-web/content-pool/README.md) | 所有作品的唯一编辑来源、独立展示顺序及生成目录的维护规则。 |
| [`reader-web/CHANGELOG.md`](reader-web/CHANGELOG.md) | 面向读者体验的未发布与版本变更。 |
| [`scripts/build-static-preview.mjs`](../../scripts/build-static-preview.mjs) | 从网页源码构建精简的静态发布包；输出到仓库根 `dist/cloudflare-preview/`。 |

产品本体、路线图、权利审查结论、商业判断和外部研究不在此重复，分别见 [`docs/products/distribution/`](../../docs/products/distribution/)、[`docs/business/`](../../docs/business/)、[`docs/research/`](../../docs/research/)。

网页工具类样式由 `reader-web/reader-tailwind.css` 生成到 `reader-web/reader-utilities.css`。修改 HTML 中的 Tailwind 类后，执行 `npx --yes tailwindcss@3.4.17 -i products/distribution/reader-web/reader-tailwind.css -o products/distribution/reader-web/reader-utilities.css --content products/distribution/reader-web/index.html --minify`，并将生成文件一起提交；读者页面无需运行时样式 CDN。
