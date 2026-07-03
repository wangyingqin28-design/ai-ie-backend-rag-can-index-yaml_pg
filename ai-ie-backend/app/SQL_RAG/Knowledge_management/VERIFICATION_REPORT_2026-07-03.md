# 文件解析与 DeepSeek 提取入库链最终验证报告

验证时间：2026-07-03（Asia/Shanghai）

## 最终结构

- `backend/public_program_files/runtime/app`：两条链唯一的公共实现和唯一运行时 `.env`。
- `backend/File_parsing/parsing_logic/runtime/file_parsing_chain`：只保留 5 个文件解析薄入口。
- `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain`：只保留提取、ORM、数据库服务和路由专属实现。
- 两个业务目录均不存在 `runtime/app`，旧 `annotations` 目录已全部删除。
- 跨三个所有权目录的相同 Python 文件散列组：0。

## 全量定义与逐行注释审计

- 公共源模块：17；公共源 `def/class`：73。
- 提取链独占源模块：9；独占源 `def/class`：45。
- 项目内传递依赖源定义总数：118；目标缺失：0；额外：0。
- 运行时 Python 文件：39。
- 实际代码物理行：2251。
- 带日期到秒、具体作用和修改依据的中文内联说明行：2251。
- 每条代码严格对应一条紧邻说明；连续说明、孤立说明、空白行和独立原注释均为 0。
- 本次全量修正时间：`2026-07-03 18:11:51`；不合规代码行：0；覆盖率：100%。
- 所有跨行字符串已等价改写；源和目标 AST 字符串值逐项相等，提示词语义未改变。
- 三处运行时 `compileall`：退出码 0。

## 真实录音、硅基流动与数据库

源项目代码引用的历史文件
`E:/录音文件/录音文件/1蔡小姐/20260505_151407详和开会2.m4a`
已不存在；源 `app` 只留下 `_raw.md` 等历史输出，上传逻辑会在 `finally`
删除原音频。按已批准方案，实测使用本机现存真实通话录音：

`C:/Users/DELL/Documents/WeChat Files/wxid_ahul2j69cxzm22/FileStorage/File/2025-12/18859060061(18859060061)_20251217154314.mp3`

- 文件长度：40704 字节；MP3 文件头：`FF FB`。
- FFmpeg：8.1.2，实际完成 WAV 分片。
- 硅基流动语音模型：`FunAudioLLM/SenseVoiceSmall`。
- 转录分片：1；转录文本长度：61；报告只保存文本 SHA256，不保存全文。
- DeepSeek：`deepseek-ai/DeepSeek-V4-Pro`，实际输入为上述录音的 API 转录结果，未替换为手写文本。
- 实际入库：`AI_YuanShishuju` 1 行、`AI_Wendajilu` 1 行、`AI_Yitu` 1 行。
- 截图字段 `AI_WenTi`、`AI_DaAn`、`AI_Biaozhu`、`WenTiYuanWen`、`DaAnYuanWen`、`WenTi_true`、`DaAn_true`、`Biaozhu_true` 全部非空。
- 问答和意图均通过 `Yssj_id` 关联原文。
- 测试后按问答、意图、原文顺序清理，三表剩余测试行：0。
- 另一次固定文本 DeepSeek/数据库回归也通过并清理为 0。

## 配置与安全

- 源 `.env` 仅字节复制到 `public_program_files/runtime/.env`。
- 两个业务运行时不再保存 `.env` 副本。
- 公共 `.env` 被 `.gitignore` 排除；Git 跟踪的运行时 `.env`：0。
- 报告未写入 API Key、数据库密码或完整连接串。
- 所有敏感配置仅在真实测试进程中读取。

## 最终测试证据

- Python 全套（包含真实语音、真实 DeepSeek、真实 PostgreSQL）：49 passed，0 failed，0 skipped。
- Node.js 既有基线：13 passed，0 failed。
- 注释严格一对一规则由独立回归测试覆盖，包括定义/赋值目标点名和乱码扫描。
- 生成器连续运行两次的运行时/清单综合 SHA256 均为
  `0bda2453c460703ac98f0012c1d4ef52a003d9a16efc1b49a8733ad519aea2d8`。
- 内存 Qdrant 写入通过；配置的真实 `yulith:6333` 仍为
  `ConnectionRefusedError`，没有虚报为已连通。

## 证据文件

- `backend/public_program_files/manifests/ownership.json`
- `backend/public_program_files/manifests/inline_comment_coverage.json`
- `backend/File_parsing/parsing_logic/manifests/live_audio_transcription_report.json`
- `backend/File_parsing/parsing_logic/manifests/real_qdrant_probe.json`
- `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/manifests/live_audio_database_report.json`
- `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/manifests/live_test_report.json`
