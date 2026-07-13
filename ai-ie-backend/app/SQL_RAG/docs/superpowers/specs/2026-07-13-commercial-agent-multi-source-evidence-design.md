# 商业化 Agent 多源证据全链路兼容设计

## 1. 背景与现状证据

当前商业化 Agent 的稳定主链为：

`qwen_planner -> sql_rag_retrieve -> sql_rag_graph_expand -> sql_rag_memory_read -> sql_rag_business_action -> qwen_planner -> answer_verifier -> final_answer_renderer`

现有实现已经能够从主 Qdrant collection 和克隆 Qdrant collection `wkt_prasing_extra_dev` 取回候选，并让克隆候选进入检索选择与 Prompt Builder。但是代码和测试证据表明，克隆证据目前只停留在检索结果中：

- 图谱扩展只接收 `source_chunk_ids`，不了解 `source_pk`、`source_table`、`mapping_profile_name` 和完整 payload。
- 记忆读取只接收 `user_id` 与 `query`，没有本轮证据身份。
- 业务动作只接收通用 `_agent_context`，没有强类型证据上下文。
- Prompt Builder 只输出 `chunk_id` 和文本，没有稳定来源契约。
- 校验器、最终渲染器和审计回放只保留旧的 chunk 标识，无法证明克隆库证据经过了每个节点。
- 当前健康检查只验证主 collection，不能证明 `wkt_prasing_extra_dev` 已接入商业化主链。

因此，本设计不是增加第三条孤立检索分支，而是在不改变既有节点顺序和下游业务语义的前提下，为全部节点建立统一、可追踪、可降级的多源证据契约。

## 2. 目标与成功标准

### 2.1 功能目标

1. 主库与克隆库候选使用同一套证据模型，公平参与候选配额、统一评分、去重与质量门控，不写死数据库优先级。
2. 被选中的主库或 `wkt_prasing_extra_dev` 证据，从检索开始一直贯穿图谱、记忆、业务动作、Prompt Builder、校验器、最终渲染器、审计与回放。
3. 四份 profile 继续作为数据契约来源，字段名和值保持原样：
   - `krauss_ai_ie_dev.yml`
   - `krauss_ai_ie_raw_data_dev.yml`
   - `wkt_prasing_extra_qa_dev.yml`
   - `wkt_prasing_extra_raw_data_dev.yml`
4. 克隆服务不可用时，主链按明确规则降级；当最终回答依赖克隆证据而该证据在后续节点失效时，系统不得悄悄生成无依据答案。
5. 全量启动脚本和健康接口能够分别证明主库、克隆 PG、主 Qdrant、克隆 Qdrant、Agent 后端和 WebUI 的真实可用状态。

### 2.2 验收标准

- 对仅在 `wkt_prasing_extra_dev` 中存在的测试问题，检索阶段能选中克隆证据。
- 同一个 `source_table + source_pk` 在多路检索中只保留一份，且保留完整来源和最佳评分信息。
- 每个商业化节点的运行标记都携带同一 `evidence_id`，能够在一次 trace 中连续追踪。
- Prompt Builder 中包含克隆证据正文以及受控的来源元数据。
- 校验器能够引用该证据作支持度判断，最终渲染结果包含可追溯来源列表。
- 主库与克隆库冲突时，选择结果只由标准化评分、来源最低配额、质量门控和去重规则决定。
- 克隆库故障时：如果主库证据充分则降级完成；如果回答必须依赖克隆证据则转人工或输出证据不足，不得伪造成功。
- 单元、契约、集成、全量启动和浏览器端到端验证均通过。

## 3. 不变约束

1. 不改变商业化 Agent 的节点顺序，不新增绕开既有校验器的回答分支。
2. 不改变 SQL Server 业务动作、Neo4j 扩展、三层记忆和最终渲染的既有业务语义。
3. 不修改四份 profile 的真实字段拼写，不做会产生空格或大小写漂移的字段名格式化。
4. `wdjl_id` 必须保持为 `wdjl_id`；`shuju_id` 必须保持为 `shuju_id`。
5. `AI_YuanShishuju.AI_Filebiaozhu` 继续作为原始数据向量正文；`LaiYuan`、`WenJianDiZhi`、`WenJianName`、`shuju_id` 继续作为 payload 字段。
6. 新增实现遵守用户的注释要求：每一条新增可执行代码必须有对应中文说明，并标注实施时的 `YYYY-MM-DD HH:mm:ss`，说明代码作用和设计依据；注释不得改变字段、Prompt 或运行语义。
7. 现有脏工作树中的用户改动必须保留；实施时只修改本规格列出的范围。

## 4. 方案选择

### 4.1 已选方案：统一证据信封与来源注册表

采用 `EvidenceEnvelope + RetrievalSourceRegistry + AgentEvidenceContext` 三层边界：

- `EvidenceEnvelope` 负责单条证据的稳定身份、正文、payload、评分和降级信息。
- `RetrievalSourceRegistry` 负责按配置注册主库与克隆库适配器，对调用方隐藏连接地址和 collection 差异。
- `AgentEvidenceContext` 负责把本轮候选、最终选中证据及节点处理标记贯穿整个 LangGraph 状态。

这是对现有链路改动最小且可验证性最高的方案。它不复制一条“克隆库 Agent”，也不把克隆库逻辑散落到每个节点。

### 4.2 未采用方案

1. **在每个节点内直接查询克隆库**：耦合连接配置，造成重复查询和来源身份漂移，无法保证同一证据贯穿全链路。
2. **把克隆库合并进主 collection**：破坏现有服务隔离与回滚边界，也无法验证独立数据库和独立 Qdrant 服务的真实状态。
3. **只在 Prompt Builder 拼接克隆文本**：这正是当前缺口，图谱、记忆、业务动作、校验和审计均无法追踪来源。

## 5. 核心数据契约

### 5.1 EvidenceEnvelope

`EvidenceEnvelope` 使用不可变或等价强约束数据结构，至少包含：

| 字段 | 含义 |
| --- | --- |
| `evidence_id` | `mapping_profile_name + source_table + source_pk` 的稳定摘要 |
| `collection` | 实际 Qdrant collection 名称 |
| `mapping_profile_name` | 生成该 point 的 profile 名称 |
| `source_table` | `public.AI_Wendajilu`、`public.AI_YuanShishuju` 等真实表名 |
| `source_pk` | `wdjl_id` 或 `shuju_id` 的真实值 |
| `retrieval_text` | 用于相似度检索的正文 |
| `text` | 提交给后续节点的规范正文 |
| `payload` | profile 生成的完整业务 payload，不改键名 |
| `dense_score` | 稠密检索原始分数，可空 |
| `sparse_score` | 稀疏或混合检索原始分数，可空 |
| `rerank_score` | 重排分数，可空 |
| `normalized_score` | 统一到 `[0, 1]` 的跨来源比较分数 |
| `selection_reason` | 入选或被淘汰的确定性原因 |
| `degraded` | 该来源是否处于降级状态 |
| `error_code` | 稳定错误码，可空 |

所有旧主库 chunk 也必须转换成相同证据信封；不能只为克隆库创建特殊结构。

### 5.2 AgentEvidenceContext

`AgentEvidenceContext` 保存：

- `candidate_evidence: list[EvidenceEnvelope]`
- `selected_evidence: list[EvidenceEnvelope]`
- `primary_evidence_id: str | None`
- `source_health: dict[str, SourceHealth]`
- `node_marks: dict[str, EvidenceNodeMark]`
- `degradation_decision: str | None`

LangGraph 状态只保存可 JSON 序列化值；跨 checkpoint、审计和回放时保持字段一致。

### 5.3 去重、配额与质量门控

1. 每个已启用来源先独立取回最低候选配额，避免某个 collection 因分数量纲占满候选池。
2. 各来源分数在来源内部标准化，再进入统一重排。
3. 以 `source_table + source_pk` 为业务去重键；同键多候选保留重排分数最高者，并合并检索模式与原始分数。
4. 不设置主库或克隆库固定优先级。
5. 质量门控综合 `normalized_score`、最小绝对分数、第一名与第二名差值和正文完整性。
6. 所有选择理由写入 `selection_reason` 和审计事件，确保结果可复现。

## 6. 组件边界

### 6.1 RetrievalSourceRegistry

职责：

- 从现有运行配置注册主 collection、混合 collection 与 `wkt_prasing_extra_dev`。
- 返回统一的 `RetrievalSourceAdapter` 列表。
- 独立执行来源健康探测，记录延迟、错误码和 collection 状态。
- 不负责候选评分、Prompt 构造或业务动作。

适配器输出必须直接转换成 `EvidenceEnvelope`，禁止节点继续读取裸 Qdrant payload。

### 6.2 EvidenceFusionService

职责：

- 执行来源配额、标准化、业务键去重、重排和质量门控。
- 输出完整候选集和最终选中集。
- 保持当前 dense baseline 与 hybrid shadow 的行为，但把克隆来源纳入同一确定性规则。

### 6.3 EvidenceContextCodec

职责：

- 在强类型对象、LangGraph 字典、checkpoint JSON、审计 JSON 和回放 JSON 之间无损转换。
- 校验必须字段和 profile 原始键名。
- 对超长 payload 只在 Prompt 展示层做裁剪；审计中保留稳定摘要和来源身份。

## 7. 全链路数据流

### 7.1 检索节点 `sql_rag_retrieve`

1. Planner 生成检索计划。
2. 注册表并行调用主库、混合检索和克隆库适配器。
3. 适配器生成统一候选。
4. 融合服务执行配额、标准化、去重、重排和门控。
5. 节点把 `AgentEvidenceContext` 写入图状态与审计，不再只返回 `best_answer` 和裸 chunk。

### 7.2 图谱节点 `sql_rag_graph_expand`

- 对带有既有 `chunk_id` 的主库证据继续走原 Neo4j/SQL 图谱扩展。
- 对只有 `source_table + source_pk` 的克隆证据，先通过独立的 `EvidenceGraphAnchorResolver` 查找可用图谱锚点。
- 找不到锚点时标记 `not_applicable`，保留原证据，不把“没有图谱映射”误判为检索失败。
- 图谱节点标记必须记录输入和输出的 `evidence_id`、实体、边、延迟和降级原因。

### 7.3 记忆节点 `sql_rag_memory_read`

- 继续按 `user_id + query` 读取既有三层记忆。
- 同时接收只读的 `AgentEvidenceContext`，把 `evidence_id` 与来源摘要写入本轮 episode/checkpoint 上下文。
- 不把完整业务 payload 永久复制到记忆库，避免膨胀；仅保存身份、摘要和必要引用。
- 删除当前测试中“记忆上下文不得包含 selected_evidence”的旧限制，改为允许受控证据引用。

### 7.4 业务动作节点 `sql_rag_business_action`

- 在现有 `_agent_context` 中加入受控的 `selected_evidence` 摘要。
- 业务工具只能读取 allowlist 字段：`evidence_id`、`source_table`、`source_pk`、`mapping_profile_name`、正文摘要和业务所需 payload 子集。
- 不改变既有 SQL Server 动作名称、参数和事务语义。
- 审计事件关联 action id 与证据 id，证明业务动作使用了哪条证据。

### 7.5 Prompt Builder 与第二次 Planner

- Prompt Builder 输出按质量排序的证据块，每块包含：正文、来源表、来源主键、profile、collection 和证据 id。
- payload 只按 profile allowlist 展示，保持 token 预算；字段值不得改写。
- 第二次 Planner 接收同一 `AgentEvidenceContext`，禁止重新生成另一套来源身份。

### 7.6 校验器 `answer_verifier`

- 对答案声明逐条匹配 `selected_evidence`，输出支持证据 id 与不支持原因。
- 克隆来源不可用但主库证据充分时允许降级通过。
- 主要证据来自克隆库且在校验阶段缺失、损坏或无法回放时，返回 `needs_human=True` 或证据不足，不允许无证据完成。

### 7.7 最终渲染器 `final_answer_renderer`

- 保持现有回答正文格式。
- 在结构化响应和解析过程区域增加 `answer_sources`，包含 `evidence_id`、collection、source table、source pk、profile 与选择理由。
- 保留旧 `answer_source_chunk_ids` 字段用于兼容，但新证据不得伪造 chunk id。

### 7.8 审计、回放与可观测性

- 每个节点写入同一 trace id、evidence id 集合、输入/输出摘要、延迟和降级状态。
- 回放时使用记录的证据身份重新读取来源；若 point 已删除，明确标记历史证据缺失。
- WebUI 解析过程展示各来源候选数、入选证据、质量门控原因及节点级证据连续性。

## 8. 配置与 profile 契约

### 8.1 profile 原样约束

- `krauss_ai_ie_dev.yml`：`id_field=wdjl_id`，QA 正文与 payload 按现有字段。
- `krauss_ai_ie_raw_data_dev.yml`：`id_field=shuju_id`，向量正文为 `AI_Filebiaozhu`。
- `wkt_prasing_extra_qa_dev.yml`：来源表 `public.AI_Wendajilu`，目标 collection `wkt_prasing_extra_dev`。
- `wkt_prasing_extra_raw_data_dev.yml`：来源表 `public.AI_YuanShishuju`，目标 collection `wkt_prasing_extra_dev`。

Agent 运行时不解析 YAML 生成新字段名；它只消费 Qdrant point 顶层契约与嵌套 payload。启动时增加 profile 契约校验，发现空白字段、缺失 trace key 或主键拼写漂移时直接报告配置错误。

### 8.2 运行配置

商业化 Agent 配置增加来源列表而不是继续增加单个硬编码 collection 属性。每个来源配置至少包含：名称、Qdrant URL、collection、候选配额、超时、是否必需和允许的 profile 集合。

默认来源：

- 主库 collection（现有配置）
- 主库 hybrid collection（现有配置）
- `wkt_prasing_extra_dev`，Qdrant `http://127.0.0.1:6335`

## 9. 错误处理与降级矩阵

| 场景 | 行为 |
| --- | --- |
| 克隆 Qdrant 不可达，主库证据充分 | 记录 clone degraded，主链继续 |
| 主库不可达，克隆证据充分 | 记录 primary degraded，允许克隆证据继续 |
| 两边均不可达 | 检索失败，转人工或返回依赖不可用 |
| 某证据缺少 `source_pk/source_table/profile` | 候选隔离，不进入最终选择；健康接口报告契约错误 |
| 克隆证据没有图谱锚点 | 图谱阶段 `not_applicable`，保留证据继续 |
| 被选证据在校验/回放时已删除 | 校验不通过并转人工，不静默替换 |
| 同业务键多条 point | 去重后保留最佳分数，审计记录被合并候选 |
| profile 字段出现空格或拼写漂移 | 启动契约校验失败，明确指出字段和文件 |

## 10. 测试设计

### 10.1 单元与契约测试

- `EvidenceEnvelope` 构造、序列化、必填字段和稳定 id。
- 主库与克隆库候选适配。
- 来源配额、分数标准化、`source_table + source_pk` 去重、无固定优先级。
- profile 字段精确匹配，重点防止 `wdjl_ id` 等空格回归。
- 图谱锚点命中与 `not_applicable`。
- 记忆证据引用、业务 allowlist、Prompt token 裁剪、校验来源支持度、渲染兼容字段。

### 10.2 节点链路测试

使用仅存在于 `wkt_prasing_extra_dev` 的唯一问题，逐个断言：

1. `sql_rag_retrieve` 选中克隆证据。
2. `sql_rag_graph_expand` 保留相同 evidence id。
3. `sql_rag_memory_read` 记录相同 evidence id。
4. `sql_rag_business_action` 的审计动作关联相同 evidence id。
5. Prompt Builder 包含该证据正文与来源。
6. 第二次 Planner 不丢失证据。
7. `answer_verifier` 使用该证据完成支持度判断。
8. `final_answer_renderer` 输出该来源。

### 10.3 故障与公平性测试

- 主库与克隆库冲突，不设置固定优先级，评分更优者胜出。
- 每个来源最低候选配额生效。
- 主库、克隆库分别中断时的降级矩阵。
- 被选克隆 point 在检索后、校验前删除时必须转人工。
- 同键重复 point 的去重与审计。

### 10.4 真实服务验证

1. 启动全部既有基础设施、克隆 PG `15433`、克隆 Qdrant `6335`、Agent 后端与 WebUI。
2. 校验四份 profile 和两个 collection 的点数、payload 与追踪字段。
3. 通过真实 Agent HTTP 接口提问唯一克隆问题。
4. 检查完整节点 trace 和最终 `answer_sources`。
5. 浏览器打开 Agent WebUI，确认解析过程显示全部节点且无 `model_quality_failed`、无无依据转人工。
6. 再运行主库专属问题，确认既有主库链路无回归。

## 11. 健康检查与启动验收

商业化健康状态新增：

- `retrieval_sources.primary.ready`
- `retrieval_sources.hybrid.ready`
- `retrieval_sources.wkt_prasing_extra.ready`
- 每个来源的 URL、collection、point count、contract status 和最近错误。

`start-latest-full-stack.ps1` 仍负责全量服务，不减少任何服务；其完成条件必须包含克隆 PG、克隆 Qdrant、四份 profile 同步、Agent 健康和 WebUI 代理健康。脚本不得只因端口监听就判定成功，必须调用健康接口与最小检索探针。

## 12. 实施文件边界

预计新增或修改范围：

- `app/SQL_RAG/overall_planning/agent_Business_Brain/agent_contracts.py`
- 新建证据契约、来源注册表、融合服务和序列化组件的聚焦模块
- `app/SQL_RAG/overall_planning/agent_Business_Brain/business_brain_runtime.py`
- `app/SQL_RAG/overall_planning/agent_Business_Brain/business_brain_service.py`
- 现有商业化 Agent 单元、契约、集成和回归测试
- `app/SQL_RAG/start-latest-full-stack.ps1`
- 必要的验证工具与设计/验证报告

四份 profile 只有在契约测试证明存在错误时才允许修改；不得为了 Agent 接入重命名业务字段。

## 13. 完成定义

只有同时满足以下条件才能报告完成：

1. 代码实现、逐行中文注释和时间依据审计通过。
2. 全部新增测试先失败后通过，既有商业化回归测试通过。
3. 全量服务启动成功，所有健康接口与最小探针通过。
4. 主库专属问题与克隆库专属问题均完成全部 Agent 节点。
5. 克隆库专属问题的同一 `evidence_id` 在检索、图谱、记忆、业务动作、Prompt、校验、渲染和审计中连续可见。
6. 最终答案有证据支持且未触发无依据的 `model_quality_failed`。
7. 四份 profile 的真实字段名、collection 和 payload 契约未发生漂移。
