# 分发 Demo 的推荐系统研究

日期：2026-09-28
状态：技术与产品研究；未批准接入线上服务或真实用户数据

## 问题范围

评估当前本地分发 Demo 是否能加入推荐机制。当前内容池为 23 部预写作品；主要条目有标题、作者、简介、标签、时长、节点/结局数量、主题颜色和封面。更有辨识度的是作品内部的节点图：每个非结局节点通常有 `text`、`exits`（可达目标）和 `labels`（向读者呈现的选项文案），终点另有 `isEnding`、`title`、`summary`。当前格式尚未给每个选项声明其决策含义、情境或取舍标签。Demo 能保存少量当前设备本地状态，但没有跨用户行为、曝光/选项呈现日志或故事片段满意度标注。

本研究关心三件事：推荐算法的常见路线、开源实现各自解决什么问题、哪些路线在 23 部作品和单机 Demo 阶段可以诚实验证。

## 开源资源

| 项目 | 上游说明 | 对本 Demo 的价值 | 当前结论 |
|---|---|---|---|
| [Microsoft Recommenders](https://github.com/recommenders-team/recommenders) | Jupyter 示例与最佳实践，覆盖数据准备、传统/深度模型、离线评估及部署 | 学习算法比较、指标和端到端实验流程 | 研究资料库，不作为前端依赖；示例环境及依赖组合较重 |
| [RecBole](https://github.com/RUCAIBox/RecBole) | PyTorch 推荐研究框架；仓库自述支持 94 种算法、44 个基准数据集，含标准评估协议 | 比较协同过滤、序列、上下文、知识型模型，后续做离线基准 | 研究/benchmark 首选，不适合嵌入单页 HTML |
| [TensorFlow Recommenders](https://github.com/tensorflow/recommenders) | TensorFlow/Keras 上的数据准备、模型训练、评估和部署工具链；快速开始使用 MovieLens 交互数据训练 retrieval 模型 | 若未来需要大规模候选召回与排序，可研究其双塔/检索流程 | 当前无训练数据、TF 服务端与模型部署边界，不引入 |
| [LightFM](https://github.com/lyst/lightfm) | 用用户/物品特征形成混合隐式反馈模型，目标之一是缓解新用户或新物品的冷启动 | 研究“内容元数据 + 用户交互”的混合方式；概念上比纯协同过滤更接近小内容池 | 值得后续离线试验；仍需一批具有代表性的交互数据，不因有 tags 就自动获得可靠个性化 |
| [implicit](https://github.com/benfred/implicit) | ALS、BPR、Logistic Matrix Factorization、基于邻居的隐式反馈算法 | 若积累足量收藏、进入、完成等行为，可用于 Python 离线比较 | 当前人群/交互矩阵缺失，不适合训练；不接入浏览器 |
| [LensKit for Python](https://github.com/lenskit/lkpy) | 面向研究和教育的推荐算法训练、运行与评估工具 | 学习实验设计与可复现评估 | 可作第二评估参考；不是线上服务或 HTML 库 |
| [Gorse](https://github.com/gorse-io/gorse) | Go 推荐引擎，组合最新、相似项、协同过滤、多模态向量及 REST API，依赖存储/缓存与后台训练流程 | 未来分发产品的候选召回/服务层参考，且能覆盖多来源候选 | 对 23 部静态内容与单用户 Demo 明显过重；现在不部署 |
| [Metarank](https://github.com/metarank/metarank) | 用点击等事件与特征训练个性化 LambdaMART 排序，可独立运行 API，状态可用 Redis | 值得借鉴曝光/互动事件模型和“先召回、再重排”边界 | 现在缺事件量、候选特征和多个体验者，不引入排序服务 |
| [MABWiser](https://github.com/fidelity/mabwiser) | 用于上下文多臂老虎机策略的 Python 研究库，包含仿真比较；Mab2Rec 示例用于内容/上下文推荐 | 未来当产品在已知候选间主动探索、并能定义可靠回报时作策略参考 | 读者选择的是作品内分支，不自动等于推荐系统的满意度回报；当前不引入 |
| [Vowpal Wabbit / learn_to_pick](https://github.com/VowpalWabbit/learn_to_pick) | 面向上下文老虎机场景的在线选项决策与反馈学习，含新闻推荐示例 | 可参考“给定候选 + 上下文 + 决策 + 后续回报”的事件建模 | 同样需要可解释的奖励信号；不能把剧情后果/读者选项直接当成用户满意度 |

## 关键技术事实与来源评估

1. 推荐系统开源资源可分成“算法研究/评测工具箱”和“可部署推荐服务”两类。Microsoft Recommenders、RecBole、LensKit 偏实验与评估；Gorse、Metarank偏服务化。仓库自述的算法数量、支持能力和架构仅代表上游项目声明，不证明它们适合本项目。
2. `implicit` 的 ALS/BPR 等方法基于用户—物品隐式反馈矩阵；LightFM 允许物品和用户特征参与混合表示。它们能提供合适的技术起点，却不能补足缺失的真实交互信号。
3. TFRS 的官方快速开始使用大量 MovieLens ratings 训练，并拆分训练/测试集；这说明其典型验证前提和当前静态内容池有明显差异。
4. Gorse 和 Metarank 都提供 API、事件导入或后台训练能力。它们解决的是服务与在线排序问题，不是给一个静态 HTML Demo 安上“机器学习”就自然得到更好的推荐。
5. 与本项目最贴近的学术先例是 Yu 与 Riedl 的 *A Sequential Recommendation Approach for Interactive Personalized Story Generation*（AAMAS 2012）。其 Prefix-Based Collaborative Filtering（PBCF）在分支故事中建模“故事至今”的序列偏好；论文指出，体验评价依赖此前的 plot points，不能只看孤立的下一个节点。它收集故事片段评分并依赖多读者反馈，而不是直接把读者选了哪个方向等同于喜好；其 Drama Manager 还会按偏好选择后续情节，与本项目要保护的作者定义分支/用户能动性并不完全相同。
6. MABWiser、`learn_to_pick` 是“从候选中挑选并用回报更新策略”的 contextual bandit 方向。剧情选择能提供条件性偏好信息，但不天然是回报：选了冒险分支不证明读者满意，救援失败也不证明作品不合口味。除非补充独立的体验回馈并定义目标，不能直接把 bandit 当作首版算法。
7. 可借鉴的原始记录单位应是“在某条故事前缀、面对这组实际展示选项，读者选择了其中一项”。孤立记录一个方向编号或标签会丢失情境；不记录未选的同场选项，也无法知道当时的比较关系。

来源包括项目官方 GitHub 仓库/README 与一手学术论文，核对日期 2026-09-28。项目能力描述可信度中高；许可证、兼容版本和维护状态在正式采用前仍须重新核对。PBCF 论文对互动叙事序列偏好的直接相关性高，但年代较早、实验域有限，不能据此声称当前推荐方案已验证。模型是否提升信息雨体验仍是本项目假设。

## 暂时排除

- 纯协同过滤：没有多用户行为矩阵，无法从当前 Demo 中学到“相似读者喜欢什么”。
- 深度/向量/LLM 推荐：23 部小池、特征较薄且没有相关性标注，模型复杂度大于可验证信号；还会引入运行依赖、推理/维护成本和错误的智能感。
- 以点击或收藏数假装热门：当前只有本地状态，不存在全体热度统计；用模拟数字会把假数据包装成社会证明。
- 把方向编号（left/right/up）当作可迁移偏好：不同节点与作品中方向位置不承载稳定语义。
- 把单次选项直接等同于满意、人格或价值判断：它只说明在当前故事前缀和选项集合下作了这次选择。
- 用故事内部偏好模型自动改写/代选现有分支：当前内容图已由作品定义可达路径；要验证的是推荐，不应默默夺走读者选择权。

## 研究链接

- Microsoft Recommenders：<https://github.com/recommenders-team/recommenders>
- RecBole：<https://github.com/RUCAIBox/RecBole>
- TensorFlow Recommenders：<https://github.com/tensorflow/recommenders>
- LightFM：<https://github.com/lyst/lightfm>
- implicit：<https://github.com/benfred/implicit>
- LensKit：<https://github.com/lenskit/lkpy>
- Gorse：<https://github.com/gorse-io/gorse>
- Metarank：<https://github.com/metarank/metarank>
- MABWiser：<https://github.com/fidelity/mabwiser>
- Vowpal Wabbit `learn_to_pick`：<https://github.com/VowpalWabbit/learn_to_pick>
- Yu & Riedl, “A Sequential Recommendation Approach for Interactive Personalized Story Generation” (AAMAS 2012)：<https://aamas.csc.liv.ac.uk/Proceedings/aamas2012/papers/2A_3.pdf>
