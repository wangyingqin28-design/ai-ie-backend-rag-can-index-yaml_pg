# 文件解析链执行顺序

- 迁移时间：2026-07-03 14:26:27
- 边界：项目内传递依赖全部纳入；第三方包内部实现排除。

## 主路径

1. `processor.process_file` 调用 `file_utils.validate_file` 校验路径。
2. `file_utils.get_file_type` 按扩展名选择 image/document/audio/text。
3. 图片分支调用 `image_service.recognize_image` 或 `ocr_image`，最终经 `llm_client.chat_complete` 访问硅基流动视觉模型。
4. 文档分支调用 `document_service.process_document_file`，再经 Docling 转换器输出 Markdown/JSON。
5. 音频分支调用 `audio_long_service.transcribe_long_audio`，经 FFmpeg 分片后由 `audio_service.transcribe_audio` 访问硅基流动转录接口。
6. 文本分支调用 `document_service.process_text_file` 读取 UTF-8 内容。
7. 入口统一组装 success、file、engine、mode 与 result；可选调用 `export_service`。
8. `process_folder` 扫描支持文件并逐个回到 `process_file`，单文件异常不会中断批次。
9. `to_index_item` 把解析结构转换为可索引文本。
10. Qdrant 包装入口延迟导入 `knowledge_index_service`，补充 kb/file/mode 元数据后调用 `vector_index_service.upsert_items_to_qdrant`。
11. `config`、`vectorstore` 与 `query` 模块提供配置、连接器和查询数据结构。
