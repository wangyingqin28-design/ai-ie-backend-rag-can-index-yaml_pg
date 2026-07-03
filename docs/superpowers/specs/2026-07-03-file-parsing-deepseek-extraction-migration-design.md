# 文件解析与 DeepSeek 提取入库链路全量迁移设计

## 1. 目标

对源项目中的 `app/ai/processors/processor.py` 与
`app/services/ai/extraction/process_service.py` 做完整执行链分析、分支测试、真实外部服务验证和项目内传递依赖迁移。
迁移结果分别落入用户指定的两个 SQL_RAG 目录，并提供可运行镜像、执行顺序、定义清单、测试证据和逐物理行中文注释台账。

## 2. 已确认边界

- 纳入两个入口文件直接或间接触发的全部项目内依赖，包括路由、图片/文档/文本/音频分支、导出、Qdrant、配置、提示词、模型客户端、ORM 模型、数据库会话和 ID 生成器。
- 跟踪普通导入、相对导入、函数内延迟导入及运行时实际调用。
- 包含已纳入模块内的全部 `def`、`async def` 和 `class`，避免只摘取局部函数后遗漏辅助定义。
- 排除 FastAPI、SQLAlchemy、OpenAI、Docling、LlamaIndex、Qdrant Client 等第三方包内部实现；保留对第三方包的调用边界和依赖说明。
- 不修改与本任务无关的目标仓库现有改动。

## 3. 已发现的源代码阻塞

`app/ai/processors/document_service.py` 只有 1547 字节，文件末尾停在 UTF-8 中文字符的中间，源码在 `build_docling_converter` 的文档字符串内被截断。
这会使 `processor.py` 在模块导入阶段失败，任何文件类型都无法进入分发逻辑。

恢复策略：

1. 先按原始字节备份损坏文件并记录 SHA256。
2. 以同一工作区中结构和函数签名一致的完整 `app/ai/vlmLI/document_service.py` 为恢复依据。
3. 保留损坏文件中仍可验证的模块说明、导入、两个安全导出函数和 `build_docling_converter` 前缀。
4. 恢复转换器、Docling 解析、统一文档入口、LlamaIndex 问答入口和纯文本入口。
5. 用导入失败测试建立 RED 证据；恢复后运行语法、导入和行为测试建立 GREEN 证据。

## 4. 迁移结构

### 4.1 第一条链：文件解析

目标根目录：

`ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/File_parsing/parsing_logic`

内容：

- `runtime/`：保持模块职责与导入关系的可运行自包含镜像。
- `annotations/`：每个运行文件对应一份逐物理行中文注释台账，记录原文件、原行号、精确到秒的迁移时间、该行作用和纳入依据。
- `manifests/execution_order.md`：按已验证运行顺序描述所有分支。
- `manifests/definitions.json`：模块、类、函数、起止行、调用者和测试覆盖点。
- `manifests/source_hashes.json`：恢复后源文件及迁移文件 SHA256。
- `tests/`：第一条链的隔离分支测试、导入测试、Qdrant 边界测试和完整性测试。

### 4.2 第二条链：DeepSeek 提取与入库

目标根目录：

`ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts`

采用与第一条链相同的 `runtime/`、`annotations/`、`manifests/` 和 `tests/` 结构。第二条链保留自己的完整解析依赖副本，使其不依赖第一条目标目录即可复现“上传到入库”的全过程。

## 5. 注释规则

- 可运行代码保持提示词字符串、SQLAlchemy 字段名和第三方调用参数不变，防止为了注释而改变业务语义。
- 模块、类、函数及关键分支在运行文件中增加中文说明。
- 每个运行文件额外生成逐物理行注释台账；源文件中的空行、多行字符串和提示词正文也逐行登记，不跳号。
- 台账格式统一为：`源行号 | 迁移时间 YYYY-MM-DD HH:mm:ss | 作用 | 理由/调用依据 | 原始代码`。
- 注释生成后校验台账行号集合与源文件物理行号集合完全相等。

## 6. 执行链验证

### 6.1 第一条链

验证顺序：文件校验 → 文件类型识别 → 图片识别/OCR、Docling 文档解析、文本读取、长音频切片与转录 → 标准结果组装 → 可选导出 → 索引项转换 → 可选 Qdrant 写入。

隔离测试覆盖所有分支与失败路径；外部测试验证 Docling 可用性、FFmpeg 探测、SiliconFlow 兼容客户端配置和 Qdrant 连接边界。真实 Qdrant 不可达时不得伪报成功，必须记录根因并使用本地内存实例证明写入算法，同时继续检查真实端点恢复条件。

### 6.2 第二条链

验证顺序：FastAPI 上传入口 → 临时文件保存 → 文件解析 → 原文提取 → `AI_YuanShishuju` 入库 → DeepSeek 问答提取 → 描述生成与合并 → 意图提取 → `AI_Wendajilu` 与 `AI_Yitu` 入库 → 可选导出 → 临时文件清理。

真实集成测试使用唯一测试标记和最小中文样本文本。验证 SiliconFlow 返回可解析 JSON，并查询数据库确认以下字段映射：

- 问答：`AI_WenTi`、`AI_DaAn`、`AI_Biaozhu`、`WenTiYuanWen`、`DaAnYuanWen`、`WenTi_true`、`DaAn_true`、`Biaozhu_true`。
- 原文关联：`Yssj_id` 指向本次 `AI_YuanShishuju.shuju_id`。
- 意图：`AI_YiTu`、`YiTu`、`BiaoZhu`。

测试记录验证完成后按关联顺序清理，避免污染业务数据；测试报告保留生成 ID、字段非敏感摘要和查询计数，不记录 API Key、数据库密码或完整连接串。

## 7. 完整性判定

只有同时满足以下条件才判定完成：

1. 静态 AST 闭包已跟踪普通导入与函数内延迟导入。
2. 运行时轨迹覆盖两个入口的全部可执行业务分支。
3. 源定义集合与目标定义集合逐项对比，无缺失类或函数。
4. 每个源物理行在注释台账中恰好出现一次。
5. 目标代码通过 `compileall`、导入测试、隔离流程测试和真实外部集成测试。
6. 数据库字段查询结果与截图所示目标字段映射一致。
7. 最终报告明确列出通过项、外部环境证据、修复内容和仍存在的客观限制；任何未通过项不得表述为已完成。

## 8. 安全与可追溯性

- 不在输出、注释、清单或测试日志中复制密钥与密码。
- 源损坏文件保留字节级备份和哈希，不静默覆盖证据。
- 目标仓库存在大量用户未提交改动，任务只写入两个指定目标目录、对应测试和本设计/实施文档。
- 迁移工具必须可重复执行；重复执行应得到相同定义集合和稳定目录结构。
