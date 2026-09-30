# 自供给分发内容资料

状态：活动资料库｜适用产品：分发产品｜建立日期：2026-09-30

这里集中保存与未来自供给分发内容有关的**数据、外部作品资料和思考**。当前保留经过故事闭环、节点选择和叙事参考价值初筛的 Twine/Twee 源文件快照，供后续批量内容生产寻找结构和写法灵感。单篇互动故事也可入选。它们是参考材料，不属于正在运行的[读者内容池](../../../products/distribution/reader-web/content-pool/README.md)，也不代表已决定采用任何作品的题材或机制。

## 目录

| 位置 | 内容 |
| --- | --- |
| [data/catalog.json](data/catalog.json) | 作品级索引、固定来源版本、原始路径、文件校验值及可机械读取的节点/链接计数。 |
| [works/](works/) | 一部作品一个目录；保留作者原始源文件路径，每部作品有来源说明。 |
| [notes/](notes/) | 此资料库的范围、整理判断和后续思考。 |
| [collect_twine_sources.py](collect_twine_sources.py) | 按已选作品清单重新获取公开文件的脚本；只用 Python 标准库。 |

## 首批范围

2026-09-30 的初始快照从 48 个带 `twine` 和 `interactive-fiction` 标签的 GitHub 仓库开始，初收 24 个作品或样本、223 个源文件。重审后，活动资料区现有 **7 部作品、25 个源文件**；逐项取舍见[清洗记录](notes/2026-09-30-quality-screening.md)。文件数不等于故事篇数或可玩分支数。

本批只覆盖这个明确的 GitHub 搜索样本，不代表网络上 Twine 作品总量。保留素材保持字节不变；每个文件的 SHA-256 在目录中。重新获取时使用 `python docs/research/content-supply/collect_twine_sources.py`；脚本的作品清单与路径范围已同步缩减，并锁定目前归档的来源提交，避免上游新文件未经筛选混入。《凌霄錄》仅保留 `src/story/`，因此不能单独运行原游戏。

## 命名规则

每部作品的目录与 `catalog.json` 中的 `id` 统一使用 `<GitHub 仓库拥有者>--<作品标题短名>`：全部小写，单词用 `-` 分隔，两个部分用 `--` 分隔，只含 ASCII 字母、数字和连字符。例如 `ronynn--interview-interview`、`jaymoda88--ling-xiao-lu`。非拉丁标题转写为稳定短名；同名时在短名末尾加可辨识的区分词。**仓库拥有者只是来源定位，不等于作品作者。** 显示标题保留作品原名；目录 ID 确定后不因标题文案修改而变化。首批旧目录名到新目录名的对照见[清洗记录](notes/2026-09-30-quality-screening.md)。

## 使用边界

- 查找作品时先读 [作品索引](data/catalog.json) 的标题、范围和来源，再进入对应的 `works/<作品>/source/`。
- 清洗决定及后续的结构比较、创作启发写入 [notes/](notes/)，不直接改写产品定义。
- 如需将任何灵感转成信息雨作品，先创作独立内容并走分发产品自己的内容流程；外部原始文件保持在本资料区。
- Twine 到当前内容包的字段和图结构转换，按[转换契约](../../products/distribution/twine-content-conversion.md)执行。

