ArXiv 论文列表查询 Skill
1. 核心功能
接收用户查询论文列表的指令，调用arxiv_search工具精准查询符合条件的论文列表，对返回结果进行结构化解析后，以自然语言友好呈现，并输出专业的论文总结分析。
2. 调用规则（增强版）
工具调用规范
json
{"tool":"arxiv_search","query":查询主题,"max_results":返回结果数量}
必填字段：tool（固定值arxiv_search）、query（用户查询主题）
max_results：返回结果数量（优化规则见下文）

返回结果数量规则（优化）
用户未指定数量 → 默认返回 5 篇
用户指定数量≤0 → 返回空字符串
用户指定数量 0<N≤15 → 返回 N 篇
用户指定数量 > N>15 → 自动截断为 15 篇，并在结果中告知用户 “因数量限制，已为你返回最多 15 篇相关论文”

3. 返回结果解析规则（优化）
基础呈现（多语言适配 + 结构化）
输出格式：按 “更新时间从新到旧” 排序，每篇论文单独分段，信息清晰标注：

【论文1】
标题：xxx
链接：xxx
更新时间：xxx（格式统一为YYYY-MM-DD）
摘要：xxx

LLM 主题查询优化规则
一、核心主题提取与翻译规则
1.  优先从用户提问中精准提取核心查询主题，过滤无关指令词（如“查询”“论文”“资料”“介绍”“相关”等），仅保留核心专业术语。

2.  若核心主题为中文：统一翻译为标准英文术语用于检索，确保术语符合学术界/行业通用规范。

    示例：

- “量子计算” → quantum computing

- “大语言模型” → large language model（可简写为 LLM，检索时优先使用全称）

- “查询关于量子计算的论文” → quantum computing

3.  若核心主题本身为英文：直接使用该英文术语检索，不额外翻译、不冗余补充。

二、主题不明确/模糊时的查询策略（重点优化）

当用户提出的主题过于宽泛、模糊，或仅给出大类主题（无具体细分方向）时，LLM需结合主题场景，拆解为多个**精准、相关的细分英文关键词/短语**，用于多维度检索，确保覆盖用户潜在需求，避免检索遗漏。

核心原则：基于用户模糊主题，联想其所属领域的核心细分方向、相关应用场景，提取行业通用的精准术语，不添加无关关键词。

具体示例：

- 用户提问主题：“AI金融”（模糊大类，未明确细分方向）

- 拆解检索关键词：algorithmic trading（算法交易）、quantitative investing（量化投资）、machine learning in finance（金融中的机器学习）、AI-driven risk management（AI驱动的风险管理）

- 用户提问主题：“AI医疗”（模糊大类）

- 拆解检索关键词：medical image recognition（医学图像识别）、AI-assisted diagnosis（AI辅助诊断）、machine learning in drug discovery（药物研发中的机器学习）

- 用户提问主题：“智能交通”（模糊大类）

- 拆解检索关键词：autonomous driving（自动驾驶）、intelligent traffic control（智能交通控制）、traffic prediction with AI（AI交通预测）

- 用户提问主题：“大数据分析”（模糊大类）

- 拆解检索关键词：data mining（数据挖掘）、predictive analytics（预测分析）、big data processing（大数据处理）

补充说明：拆解的关键词需与用户模糊主题高度相关，避免跨领域拆解；优先选择使用频率高、检索覆盖广的行业标准术语，不使用生僻、小众表述。注意，每次调用arxiv_search工具时，仅可以发送一个查询主题，不可以同时发送多个查询主题。若返回结果分析后与用户模糊主题不相关，那么选择不那么宽泛的关键词后重新调用查询工具。

三、回复语言规则（适配多语言查询）

1.  若用户提问以中文为主（无论主题是否模糊）：最终全部回复使用中文，包括检索结果的标题、摘要、解释等，其中摘要需翻译为中文。

2.  若用户提问以英文为主：最终全部回复使用英文，无需额外翻译。

3.  多语言混合提问：以用户表达核心意图时占比更高的语言，作为回复语言。

四、执行总原则

- 检索关键词：简洁、精准、通用，仅保留核心术语，不包含句子、指令或冗余描述。

- 主题明确时：单一精准英文术语检索；主题模糊时：多维度细分关键词组合检索。

- 术语翻译：优先遵循学术界/行业通用标准，确保检索一致性和准确性。

专业总结规则（新增结构化框架）
总结部分需包含 3 个核心维度，避免泛泛而谈：
共性关联：所有论文的共同研究领域 / 核心问题（如 “均聚焦于深度学习在计算机视觉中的应用，重点解决图像分类的精度问题”）
核心差异：论文间的关键区别（如 “论文 1 侧重卷积神经网络优化，论文 2 关注 Transformer 架构的轻量化，论文 3 聚焦小样本场景下的模型迁移”）
研究贡献 / 价值：该方向的整体贡献（如 “这批论文分别从模型效率、适用场景、精度提升三个维度推动了轻量化视觉模型在工业场景的落地应用”）
5. 异常处理（新增）
若arxiv_search工具返回空结果（无匹配论文）→ 提示 “未找到与「{查询主题}」相关的论文，建议：1. 简化关键词 2. 更换英文关键词 3. 扩大查询范围”
若工具调用失败（如网络错误）→ 提示 “暂时无法连接 ArXiv 数据库，请稍后重试”
示例演示（用户输入：查询 8 篇大语言模型微调的论文）
工具调用 JSON
json
{"tool":"arxiv_search","query":"large language model fine-tuning","max_results":8}
返回结果呈现
plaintext
【论文1】
标题：Efficient Fine-Tuning of Large Language Models with Low-Rank Adaptation
链接：https://arxiv.org/abs/2403.12345
更新时间：2024-03-15
摘要：This paper proposes a novel LoRA-based fine-tuning method that reduces memory consumption by 60% while maintaining model performance on downstream tasks...

【论文2】
标题：Parameter-Efficient Fine-Tuning for Multilingual Large Language Models
链接：https://arxiv.org/abs/2403.11234
更新时间：2024-03-10
摘要：We present a multilingual PEFT framework that supports 100+ languages, achieving better cross-lingual generalization compared to full fine-tuning...

...（共8篇）

### 论文总结
1. 共性关联：所有论文均围绕大语言模型的高效微调展开，核心目标是在降低微调成本（显存、算力）的同时，保持甚至提升模型在下游任务的表现。
2. 核心差异：论文1-3聚焦单语言模型的低秩适配（LoRA）优化，侧重显存占用优化；论文4-6研究多语言模型的参数高效微调，关注跨语言泛化能力；论文7-8探索微调与预训练数据的协同优化，解决领域适配问题。
3. 研究贡献：这批论文丰富了大语言模型高效微调的技术体系，突破了全量微调的资源限制，为大模型在中小算力场景、多语言场景、垂直领域的落地提供了可行方案。