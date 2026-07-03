# DeepSeek 提取入库链执行顺序

- 迁移时间：2026-07-03 14:26:28
- 边界：项目内传递依赖全部纳入；第三方包内部实现排除。

## 主路径

1. `vlm_router.process_any_files` 接收 FastAPI 上传参数并调用 `process_service.process_uploaded_files`。
2. 批量入口串行调用 `process_uploaded_file`；单文件先由 `_save_upload` 写入临时目录。
3. `file_utils.get_file_type` 校验类型，随后调用完整文件解析链 `processor.process_file`。
4. `_extract_raw_text` 按 document/text/audio/image 提取统一原文。
5. `raw_data_service.save_raw_text` 分片并写入 `AI_YuanShishuju`，返回 `raw_data_id`。
6. analyze/both 动作进入 `_run_fixed_audio_knowledge_extract`。
7. `extract_audio_knowledge` 依次执行问答提取、问答 JSON 解析、描述生成、描述合并、意图提取和意图 JSON 解析。
8. 所有模型请求经 `llm_client.llm_model_func` 和 `chat_complete` 访问硅基流动 DeepSeek。
9. `qa_pair_service.save_qa_pairs` 映射截图字段并写入 `AI_Wendajilu`。
10. `intent_service.save_intents` 写入 `AI_Yitu`，两表均通过 `Yssj_id` 关联原文。
11. 可选调用 `export_service.export_knowledge_extract_result` 导出 raw/qa/intent Markdown。
12. `finally` 无条件删除上传临时文件；路由返回原文、分析结果、数据库 ID 和可选解析详情。
13. 解析链中的图片、文档、音频、Qdrant、配置和连接器依赖随本链一并镜像。
