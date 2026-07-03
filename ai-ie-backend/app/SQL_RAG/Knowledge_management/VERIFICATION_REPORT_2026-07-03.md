# 文件解析与 DeepSeek 提取入库链迁移验证报告

验证日期：2026-07-03（Asia/Shanghai）

## 结论

两条执行链已按项目内传递依赖闭包复制到指定目录，并从各自私有 `runtime/app` 成功运行。源定义与目标定义逐项一致，逐物理行中文注释台账无缺行或重复。目标副本已使用自己的 `runtime/.env` 访问真实硅基流动 DeepSeek 和 PostgreSQL，并完成写入、查询和清理。

唯一外部限制是源代码硬编码的真实 Qdrant 地址 `yulith:6333` 当前拒绝 TCP 连接；DNS 解析正常，本地内存 Qdrant 写入测试成功。该状态没有被表述为真实 Qdrant 已连通。

## 源代码恢复

- 损坏文件：`app/ai/processors/document_service.py`
- 根因：文件在 `build_docling_converter` 文档字符串内被截断，末尾包含不完整 UTF-8 字符。
- 原始损坏文件备份：`document_service.py.corrupt-20260703.bak`
- 损坏文件 SHA256：`C0153552771A6575A0D23DEFBBB233874B58C753258EE6BC92BCA0BD8CD16B40`
- 恢复文件 SHA256：`B32E3983052D9D112CCE9858072F4173CFBF941A62271D117F07C2E8972D9E1B`
- 恢复定义：两个安全导出函数、Docling 转换器、Docling 解析、统一文档入口、LlamaIndex 问答入口、纯文本入口，共 7 个定义。
- 额外修复：恢复 `export_service.export_processed_result`。原 `processor.process_file(export=True)` 延迟导入该函数，但源实现被整段注释，导致导出分支必然 `ImportError`。

## 第一条链：文件解析

目标：`backend/File_parsing/parsing_logic`

经测试的顺序：

1. 文件路径校验与类型识别。
2. 图片识别/OCR、Docling 文档解析、文本读取、FFmpeg 长音频分片与转录分发。
3. 标准化解析结果组装。
4. 文件夹批处理和单文件异常隔离。
5. raw/summary Markdown 导出。
6. 文档、文本、音频、图片索引项转换。
7. Qdrant 元数据补充与写入边界。
8. 配置、LlamaIndex、向量存储连接器和查询模型依赖。

完整性数据：

- 项目内模块：17
- 源 `def/class`：73
- 目标 `def/class`：73
- 缺失定义：0
- 额外定义：0
- 源物理行：2120
- 中文逐行注释记录：2120
- 内存 Qdrant 写入：1 条文档，计数验证为 1
- 真实 Qdrant：`yulith` 解析为 `172.18.1.184`，TCP 6333 `ConnectionRefusedError`

## 第二条链：DeepSeek 提取与入库

目标：`backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts`

经测试的顺序：

1. FastAPI 上传参数进入批量与单文件调度。
2. 上传文件写入临时目录。
3. 调用完整文件解析链并统一提取原文。
4. 原文分片写入 `AI_YuanShishuju`。
5. DeepSeek 执行问答提取、描述生成、描述合并和意图提取。
6. 问答写入 `AI_Wendajilu`，意图写入 `AI_Yitu`。
7. 三表通过 `Yssj_id` 关联。
8. 可选导出和 `finally` 临时文件清理。

完整性数据：

- 项目内模块：26
- 源 `def/class`：118
- 目标 `def/class`：118
- 缺失定义：0
- 额外定义：0
- 源物理行：3592
- 中文逐行注释记录：3592

## 真实 SiliconFlow 与数据库证据

- 运行代码：第二条链目标副本，不是源目录模块。
- API 主机：`api.siliconflow.cn`
- 模型：`deepseek-ai/DeepSeek-V4-Pro`
- API Key：目标运行配置中存在；报告和日志未记录值。
- 数据库主机：`krauss`
- 连接检查：`SELECT 1` 返回 1。
- 本次验证写入：`AI_YuanShishuju` 1 行、`AI_Wendajilu` 1 行、`AI_Yitu` 1 行。
- 已验证问答字段：`AI_WenTi`、`AI_DaAn`、`AI_Biaozhu`、`WenTiYuanWen`、`DaAnYuanWen`、`WenTi_true`、`DaAn_true`、`Biaozhu_true`，全部存在有效值。
- 已验证意图字段：`AI_YiTu`、`YiTu`、`BiaoZhu`，全部存在有效值。
- 关联验证：问答和意图的 `Yssj_id` 均等于本次原文 ID。
- 清理验证：三表各删除 1 行，剩余测试记录 0。

## 测试总览

- Python 全套：40 passed，0 failed。
- Knowledge_management 既有 Node.js 基线：13 passed，0 failed。
- 两个 runtime 的 `compileall`：退出码 0。
- 配置一致性：源 `.env` 与两个目标 `runtime/.env` 字节级 SHA256 一致。
- 密钥保护：两个目标 `runtime/.env` 均被各自 `.gitignore` 排除；`.env.example` 只保留键名。
- 镜像重复生成：模块数、定义数、生成时间和行注释覆盖保持稳定。

## 审计文件

每条链均包含：

- `runtime/app`：自包含项目内依赖镜像。
- `annotations`：每个源物理行一条含时间、作用、依据和原始代码的中文记录。
- `manifests/definitions.json`：全部模块与 `def/class` 对比。
- `manifests/source_hashes.json`：源/目标 SHA256。
- `manifests/execution_order.md`：按已测试顺序记录完整执行链。
- `tests`：隔离分支、映射、清理、真实 API/数据库和 Qdrant 探测测试。
