# 知识管理两链去重与逐行内联注释设计

## 1. 目标

重构文件解析链和 DeepSeek 提取入库链，消除两个业务目录中完全重复的公共程序，将公共实现集中到：

`ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/public_program_files`

重构后：

- `public_program_files` 只存公共实现、公共配置和公共测试。
- `File_parsing/parsing_logic` 只存第一条文件解析业务入口。
- `Extraction_of_file_related_prompts` 只存第二条提示词提取、ORM 入库和路由业务。
- 所有运行 Python 程序直接包含逐代码行中文注释，不再用外置 `annotations` 目录代替内联注释。
- 重新运行真实录音转写、DeepSeek 提取、数据库字段查询和测试数据清理。

## 2. 当前问题证据

两个现有 `runtime/app` 目录共有 27 个同路径 Python 文件；忽略首行迁移时间后，27 个文件内容全部相同。第一链当前没有任何独有 Python 文件。

现有运行源码的时间戳内联注释覆盖率：

- 第一链：15 / 1579，约 0.95%。
- 第二链：23 / 2668，约 0.86%。

因此，当前结构同时存在整树重复和“外置台账存在、运行源码未逐行注释”两个问题。

## 3. 采用方案

采用严格公共层方案：

```text
backend/
├─ public_program_files/
│  ├─ runtime/app/                     # 27 个公共模块只保留一份
│  ├─ manifests/
│  ├─ tests/
│  ├─ .env.example
│  └─ .gitignore                       # runtime/.env 不进入 Git
├─ File_parsing/parsing_logic/
│  ├─ runtime/file_parsing_chain/      # 第一链薄入口
│  ├─ manifests/
│  └─ tests/
└─ Extracting_parsed_content_based_on_relevant_prompts/
   └─ Extraction_of_file_related_prompts/
      ├─ runtime/extraction_chain/      # 第二链独有实现
      ├─ manifests/
      └─ tests/
```

不采用多个 `app` namespace overlay，也不让第二链隐式加载第一链目录中的同名模块。公共 `app` 只有一份；两个业务包使用不同包名并显式导入公共层。

## 4. 程序归属

### 4.1 公共层

以下 27 个当前重复文件全部迁移到公共层，包括包标记：

- 配置：`app/config.py`
- LLM：`app/ai/llm/llm_client.py`
- 提示词：`app/ai/prompts.py`
- 文件基础处理：audio、document、export、file_utils、image、llamaindex、processor
- 向量索引：`app/ai/rag/vector_index_service.py`
- 索引服务：`app/services/ai/indexing/knowledge_index_service.py`
- 查询模型：`app/query/query.py`
- 向量连接器：`app/vectorstore/base.py`、`connector.py`、`qdrant_connector.py`
- 上述目录所需的 `__init__.py`

`processor.py` 放在公共层，因为它在两条业务链中都被真实调用，继续放在任一业务目录都会形成跨业务隐式依赖或重复副本。

### 4.2 第一链独有程序

创建 `file_parsing_chain/entry.py`，只暴露第一链业务接口：

- `parse_file`
- `parse_folder`
- `to_index_item`
- `index_file`
- `index_folder`

这些函数显式委托公共 `processor.py` 和 `knowledge_index_service.py`，用于固定第一链公开契约和运行轨迹。

### 4.3 第二链独有程序

把现有第二链独有模块整理为 `extraction_chain`：

- `process_service.py`
- `audio_knowledge_extract_service.py`
- `raw_data_service.py`
- `qa_pair_service.py`
- `intent_service.py`
- `erp_ai_models.py`
- `model_base.py`
- `snowflake_generator.py`
- `vlm_router.py`
- `__init__.py`

其中所有公共导入改为 `app.*`，所有第二链内部导入改为 `extraction_chain.*`。第二链通过公共 `app.ai.processors.processor` 完成文件解析，不复制公共代码。

## 5. 逐行内联中文注释

每个公共或业务运行 `.py` 必须满足：

1. 每个非注释代码物理行的正上方都有格式统一的中文说明：

   `# [YYYY-MM-DD HH:mm:ss] 作用：...；理由依据：...`

2. 不保留无说明空行；原空行转换为带时间的“逻辑块分隔”注释。
3. 原始注释行也保留，并在其上方增加时间、作用和依据说明。
4. 多行文档字符串和提示词不能直接插入 `#`，否则会修改字符串内容。因此将其等价改写为括号内相邻字符串片段，每个字符串片段前增加中文说明。
5. 使用 AST 和运行测试验证改写前后的字符串常量值相同，特别是 QA、描述、意图和输出格式提示词。
6. 注释时间固定为本次生成时间，精确到秒；重复生成复用清单中的时间，避免无意义变更。

完成判定：

- 所有运行 `.py` 中不存在跨多物理行的字符串 token。
- 每个非注释、非空代码行紧邻上一行均为合规时间戳中文注释。
- 内联注释覆盖率为 100%。

## 6. 录音测试样本

源项目 `app` 内没有保留任何音频二进制；只找到：

- 历史代码引用：`app/ai/deom/demo_llamaindex.py`
- 引用路径：`E:/录音文件/录音文件/1蔡小姐/20260505_151407详和开会2.m4a`
- 当前状态：该路径不存在。
- 多个历史 `_raw.md`、`_qa.md`、`_intent.md` 文件证明此前处理过 `.m4a`，但上传流程的 `finally` 已删除原临时录音。

为执行用户要求的真实录音链测试，采用本机仍存在的原始录音：

`C:/Users/DELL/Documents/WeChat Files/wxid_ahul2j69cxzm22/FileStorage/File/2025-12/18859060061(18859060061)_20251217154314.mp3`

该文件为真实 MPEG 音频，大小 40704 字节，文件头以 MP3 帧同步字节 `FF FB` 开始。测试只读取该文件，不修改或提交音频内容。

## 7. 测试流程

### 7.1 RED 测试

实施前先增加失败测试，证明：

- 两业务目录存在 27 个重复 Python 文件。
- 第一链没有独有业务入口。
- 内联逐行注释覆盖率低于 1%。
- 第二链仍依赖自己目录内的公共代码副本。

### 7.2 隔离流程测试

- 公共文件类型判断和校验。
- 文本、图片、OCR、文档、音频分发。
- 文件夹批处理与单文件错误隔离。
- 导出、索引项转换、内存 Qdrant 写入。
- DeepSeek 三套提示词顺序。
- QA、意图、原文字段映射。
- 上传临时文件成功和异常清理。

### 7.3 真实录音端到端测试

1. 检查或安装 FFmpeg，并记录可执行文件版本。
2. 读取选定真实 MP3。
3. 第一链经 FFmpeg 分片。
4. 公共 `audio_service.transcribe_audio` 使用目标公共 `.env` 中记录的 SiliconFlow Key，调用 `FunAudioLLM/SenseVoiceSmall` 转写。
5. 校验转写文本非空，并记录模型名、字符数和脱敏摘要。
6. 第二链把转写文本交给 `deepseek-ai/DeepSeek-V4-Pro`，依次生成 QA、描述和意图。
7. 写入 `AI_YuanShishuju`、`AI_Wendajilu`、`AI_Yitu`。
8. 查询截图字段并确认非空和 `Yssj_id` 关联。
9. 按问答、意图、原文顺序删除本次唯一测试记录。
10. 查询确认剩余测试记录为 0。

报告不得包含 API Key、数据库密码、完整含密连接串或完整录音转写。

## 8. 完整性与去重门禁

只有同时满足以下条件才完成：

- 公共层定义集合等于原 27 个重复模块定义集合。
- 第二链独有定义无缺失。
- 第一链入口定义全部存在并被测试。
- 两业务目录内不再出现公共模块相对路径。
- 公共层、第一链、第二链任意两层之间不存在相同内容的 Python 文件。
- 所有运行源码内联注释覆盖率 100%。
- `compileall` 通过。
- Python 全套测试 0 失败。
- 真实录音转写、DeepSeek 提取、三表查询和清理通过。
- 既有 Knowledge_management Node.js 测试保持通过。
- 三个运行目录只共享公共 `.env`；密钥文件存在但未被 Git 跟踪。

## 9. 安全清理

旧 `annotations`、两个旧重复 `runtime/app` 和旧业务测试只能在以下条件满足后删除：

1. 解析后的绝对路径位于三个明确目标目录内。
2. 新失败测试已经建立。
3. 新生成器已成功创建公共层和业务层。
4. 新结构的定义、导入和语法检查通过。

不得删除或移动 Knowledge_management 其他目录及用户未提交文件。
