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
python -X utf8 docs/research/content-supply/structure_round_02.py build
python -X utf8 docs/research/content-supply/structure_round_02.py check
python -X utf8 docs/research/content-supply/probe_breakup_state.py build
python -X utf8 docs/research/content-supply/probe_breakup_state.py check
```

`ingest` 需要已登录的 GitHub CLI (`gh auth login`)；`verify` 离线运行，仅需 Python 标准库。采集使用 GitHub Contents API 对固定提交读取文件，并核对 API 返回的 Git blob SHA；所有文件先下载并做基础节点/链接数检查，随后保留原始字节到 `works/<id>/source/<原路径>`。脚本生成每部说明、并把第二轮记录合并到总目录；重复运行时替换第二轮记录，不改首轮记录。`verify` 核对第二轮清单与总目录的成员、仓库、提交、文件路径、字节数、SHA-256 和语法计数。失败即停止，不应继续提交。

脚本不自动判定“优质”或剧情闭环；`passages`、`bracket_links` 只用于明显异常拦截。接受决定必须回到原文人工审读。完成后人工同步[作品索引](../works/README.md)和[资料库说明](../README.md)中的统计，再运行仓库验证命令并提交 Git。源文件不执行；转换为信息雨内容包须另按[转换契约](../../../products/distribution/twine-content-conversion.md)处理。

`structure_round_02.py` 将 5 部的叙事 passage 解析为各自的 `structure.json`：保留原文、原始路径和标签，拆出带文案与目标的选择，把重玩链接从结局出口剥离，记录 `StoryData` 的格式和声明起点。起点、真实结局与非叙事排除项由[人工判断清单](../data/round-02-structure-decisions.json)提供。构图后检查断链、无出口的非结局节点、仅按静态链接不可达的节点，并给每个结局保留一条带选项文案的最短**候选**路径。`check` 离线重新解析，与提交的 JSON 逐字比较，以发现源文件或规则漂移。

结构图只证明**显式文本目标的静态连通性**；条件变量、计时、`display/include`、脚本以及外部资源可能改变真实可达性。解析器将相关 passage 标为 `hasRuntimeControl` 和 `includes`，候选路径上的 `condition: needs_review` 不能当成已试玩证明。逐作品判断及真实发现的源文件断链见[结构复核](2026-10-08-round-02-structure-review.md)。这一步不删除源文件正文，也不直接生成产品内容包。

对分手循环另运行 `probe_breakup_state.py`：它解释该文件实际使用的简单 SugarCube `if/else/set`，对 `$options`、`$ending`、`$entropy` 做有界状态搜索，输出一条满足这些条件的[收束路径](../data/round-02-breakup-state-witness.json)。这仍是源码级探针，计时链接按延时后可选处理；不能替代浏览器试玩。

首轮仍由 [collect_twine_sources.py](../collect_twine_sources.py) 按当时清单复现；它会重写首轮作品索引，因而第二轮之后只用于首轮资料修复，运行后须重新补全总索引。后续新增轮次应复用固定提交与离线校验原则，先考虑合并为统一清单式工具，避免长期维持两套采集逻辑。
