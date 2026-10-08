# 第二轮 Twine 资料处理管线

状态：当前流程｜适用产品：分发产品资料库｜日期：2026-10-08

## 输入和门槛

1. 用 GitHub Code Search 发现 `.tw`、`.twee`、`.tws` 候选，记录查询与实际读取范围；搜索命中不等于入选。
2. 人工核对起点、至少两处有后果的选择、主要情境的终局和文本参考价值；遇到计时、条件宏或脚本时写清尚未验证的可达性。重复稿只留一份。取舍写入[第二轮清洗记录](2026-10-08-round-02-screening.md)。
3. 仅把通过筛选的作品写入[固定来源清单](../data/round-02-manifest.json)：稳定 ID、显示标题、GitHub 仓库、完整 40 位提交、精确文件路径、范围、入选原因和转换提醒。ID 规则见[资料库说明](../README.md)。

## 运行

在仓库根目录执行：

```powershell
python -X utf8 docs/research/content-supply/round_02_pipeline.py ingest
python -X utf8 docs/research/content-supply/round_02_pipeline.py verify
```

`ingest` 需要已登录的 GitHub CLI (`gh auth login`)；`verify` 离线运行，仅需 Python 标准库。采集使用 GitHub Contents API 对固定提交读取文件，并核对 API 返回的 Git blob SHA；所有文件先下载并做基础节点/链接数检查，随后保留原始字节到 `works/<id>/source/<原路径>`。脚本生成每部说明、并把第二轮记录合并到总目录；重复运行时替换第二轮记录，不改首轮记录。`verify` 核对第二轮清单与总目录的成员、仓库、提交、文件路径、字节数、SHA-256 和语法计数。失败即停止，不应继续提交。

脚本不自动判定“优质”或剧情闭环；`passages`、`bracket_links` 只用于明显异常拦截。接受决定必须回到原文人工审读。完成后人工同步[作品索引](../works/README.md)和[资料库说明](../README.md)中的统计，再运行仓库验证命令并提交 Git。源文件不执行；转换为信息雨内容包须另按[转换契约](../../../products/distribution/twine-content-conversion.md)处理。

首轮仍由 [collect_twine_sources.py](../collect_twine_sources.py) 按当时清单复现；它会重写首轮作品索引，因而第二轮之后只用于首轮资料修复，运行后须重新补全总索引。后续新增轮次应复用固定提交与离线校验原则，先考虑合并为统一清单式工具，避免长期维持两套采集逻辑。
