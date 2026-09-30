# Information Rain 项目入口

这里是工作恢复入口，不承载完整愿景、产品规格或商业研究。具体内容只在各自的权威文档中维护；本页负责说明去哪里读、当前哪条产品线在推进。

## 当前状态

- **产品组合**：工具 Agent 与分发产品是两条独立产品线，不能把一边的需求或实现自动套用到另一边。方向依据见[决定 0006](docs/project/decisions/0006-two-products-and-medium-validation.md)。
- **当前主线**：分发产品；工具 Agent 先预留产品和源码位置，暂不开始实施。当前阶段与下一步以[工作基线](docs/project/working-baseline.md)和[分发产品路线图](docs/products/distribution/roadmap.md)为准。
- **技术愿景**：全梦是长期技术愿景，信息雨是信息组织方法；它们不代替各产品自己的本体和规格。见[技术愿景](docs/vision/technical-vision.md)与[技术愿景本体](docs/vision/ontology.md)。

## 开始一项工作时

1. 读[当前工作基线](docs/project/working-baseline.md)，确认正在推进的产品和状态。
2. 读对应的[产品目录索引](docs/products/README.md)、产品本体和路线图。
3. 通过[项目文档索引](docs/project/README.md)查阅决定、会议、工作基线和流程；通过[研究索引](docs/research/README.md)查阅外部证据，只把当前有效材料当作实现依据。
4. 修改后按[文档与版本规则](docs/project/documentation-workflow.md)更新权威文档、索引和 Git 记录。

## 仓库地图

| 位置 | 放什么 | 规则 |
| --- | --- | --- |
| [`products/`](products/README.md) | 各产品源码、运行内容和产品专属资源 | 每个产品独立目录；独立构建、部署和版本边界。 |
| [`docs/vision/`](docs/vision/) | 长期技术愿景和愿景本体 | 不直接充当产品规格。 |
| [`docs/products/`](docs/products/README.md) | 产品业务本体、路线图和产品决策依据 | 每个产品单独维护；未知内容明确标为待确认。 |
| [`docs/business/`](docs/business/README.md) | 商业模式、市场进入、创作者交换等策划 | 保存判断和适用范围，不冒充已批准产品功能。 |
| [`docs/research/`](docs/research/README.md) | 有来源的外部研究与证据 | 按主题归档，由研究索引统一导航。 |
| [`docs/project/`](docs/project/) | 项目治理、基线、决定、会议、阶段门和流程 | 跨产品共用的协作规则。 |
| [`experiments/`](experiments/README.md) | 有界实验、试验材料和历史样本 | 当前产品源码不再放在此处。 |

## 重要入口

- [项目简报](docs/project/brief.md)
- [产品路线图总览](docs/project/roadmap.md)
- [阶段门](docs/project/stage-gates.md)
- [工作文档与版本流程](docs/project/documentation-workflow.md)
- [产品目录边界决定 0012](docs/project/decisions/0012-single-repository-product-boundaries.md)
- [技术愿景资料索引](docs/vision/README.md)
- [项目级变更日志](CHANGELOG.md)
