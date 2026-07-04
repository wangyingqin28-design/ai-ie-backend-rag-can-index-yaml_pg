# Knowledge Management 全量服务与真实录音入库设计

日期：2026-07-04
状态：待用户书面复核

## 目标

把 `Knowledge_management` 的真实后端和 WebUI 启动逻辑接入
`app/SQL_RAG/start-latest-full-stack.ps1`。执行用户指定的 PowerShell
命令后，系统必须通过新端口提供前后端服务，并使用
`新录音 4.m4a` 完成以下真实链路：

1. FFmpeg 音频处理与硅基流动语音转录。
2. DeepSeek 按现有问答、描述、意图提示词完成结构化提取。
3. 写入 PostgreSQL `AI_YuanShishuju`、`AI_Wendajilu`、`AI_Yitu`。
4. 新记录永久保留，供用户在 Navicat 中核对。

## 已确认边界

- 默认 Knowledge 后端端口：`18320`。
- 默认 Knowledge WebUI 端口：`18321`。
- 保留现有主后端、主 WebUI、资产类型服务及 Docker 依赖。
- 不把 Knowledge API 合并进 `18180` 主业务脑服务。
- 不重新复制公共解析或提取模块。
- API Key 和数据库连接从现有记录配置加载，不写入代码、日志或报告。
- 新增程序逐行添加中文注释，包含精确到秒的日期、代码作用和修改依据。
- 端到端验证产生的三表记录不清理。

## 方案选择

采用宿主机进程集成方案：

- Docker Compose 继续负责 SQL Server、Qdrant、Postgres checkpoint、
  External 服务和 Neo4j。
- `start-latest-full-stack.ps1` 使用仓库根 `.venv` 启动 Knowledge FastAPI
  后端和 Knowledge WebUI。
- 该方案复用现有 Windows FFmpeg、已安装 Python 依赖以及局域网
  PostgreSQL 连接，避免重新制作大型 Docker 镜像。

不采用以下方案：

- 全容器化 Knowledge 服务：需要重新安装 FFmpeg、Docling 和模型依赖，
  并处理 Windows 文件挂载及局域网 DNS，新增风险不服务于当前验收。
- 合并到主后端：会扩大业务脑服务职责，并违反新端口隔离要求。

## 服务结构

### Knowledge FastAPI 后端

新增独立服务入口，职责如下：

- 把 `public_program_files/runtime` 和
  `Extraction_of_file_related_prompts/runtime` 加入模块搜索路径。
- 加载公共 `.env`。
- 注册现有 `extraction_chain.vlm_router`，保留
  `POST /vlm/process` 原始批量接口。
- 提供 `GET /health`，验证服务、关键配置和 PostgreSQL `SELECT 1`。
- 提供 `POST /knowledge/parse` 单文件接口，接受真实 multipart 文件，
  调用 `process_uploaded_file(action="analyze")`。
- 把解析结果、问答项和意图项映射为 WebUI 可直接展示的结构。
- 响应中保留 `raw_data_id`、`qa_pair_ids`、`intent_ids`，用于数据库核验。

### Knowledge WebUI

现有静态页面继续由 `webui_server.py` 提供，并代理 `/api` 到 `18320`。

前端服务调整：

- `parseUpload` 使用 `FormData` 上传真实 `File`，不再只提交文件名和大小。
- 上传目标为 `/api/knowledge/parse`。
- 音频解析请求使用足够覆盖 FFmpeg、语音 API 和三轮 DeepSeek 的超时。
- 后端失败时明确显示错误，不回退到模拟解析结果。
- 本地状态兜底仅用于列表/UI 状态，不得伪造真实文件解析成功。

### 全量启动脚本

`start-latest-full-stack.ps1` 增加：

- Knowledge 后端/WebUI 端口和 URL。
- 对应进程识别与旧实例清理规则。
- 端口释放和备用端口逻辑。
- 后端/WebUI 标准输出及错误日志。
- 两个宿主机进程的隐藏启动命令。
- 后端 `/health`、WebUI `/health` 和 WebUI `/api/health` 代理健康检查。
- 最终地址、日志路径和 ready 状态输出。
- 全量 ready 判定必须包含两个 Knowledge 服务及代理。

默认使用 `18320/18321`；若被无法清理的旧进程占用，脚本只能选择空闲备用
端口并明确输出实际地址，不能把旧服务健康响应误判为新服务。

## 数据流

```text
用户或测试客户端
  -> Knowledge WebUI 18321 /api/knowledge/parse
  -> Knowledge FastAPI 18320 /knowledge/parse
  -> extraction_chain.process_service
  -> public app.ai.processors.processor
  -> FFmpeg + SiliconFlow SenseVoice
  -> DeepSeek 问答/描述/意图提示词
  -> AI_YuanShishuju
  -> AI_Wendajilu
  -> AI_Yitu
  -> 返回解析文本摘要、提取项和三类数据库 ID
```

## 错误处理

- 文件为空或扩展名不支持：返回 HTTP 400。
- FFmpeg 不存在、语音 API 失败、DeepSeek 失败或数据库失败：返回明确错误，
  WebUI 不生成模拟成功结果。
- 临时上传文件仍由现有 `finally` 清理。
- 已提交数据库记录不因后续 UI 显示错误被自动删除。
- PS1 任一 Knowledge 健康检查失败时整体启动失败，不报告全量 ready。

## 测试设计

### TDD 和本地测试

- 后端 app/health/router 导入测试。
- `/knowledge/parse` multipart 协议和 WebUI 映射测试。
- 前端必须发送真实 `FormData` 的 Node 测试。
- 前端后端失败时不得调用模拟结果的回归测试。
- WebUI 代理长请求和 Content-Type 边界转发测试。
- PS1 包含端口、启动、健康检查、日志和进程清理的静态测试。
- 新增程序逐行中文注释覆盖测试。

### 真实全量验收

1. 执行：

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
   & 'D:\wkt\ai-ie-backend-feature-rag-new (1)\ai-ie-backend\app\SQL_RAG\start-latest-full-stack.ps1'
   ```

2. 验证 Docker 依赖、现有四个宿主机服务以及 Knowledge 两个服务全部 ready。
3. 通过 `18321/api/knowledge/parse` 上传
   `D:\wkt\ai-ie-backend-feature-rag-new (1)\ai-ie-backend\新录音 4.m4a`。
4. 断言返回的音频解析文本非空，语音模型和 DeepSeek 模型符合配置。
5. 断言 `raw_data_id`、`qa_pair_ids`、`intent_ids` 均非空。
6. 使用返回 ID 查询 PostgreSQL：
   - `AI_YuanShishuju` 至少一行；
   - `AI_Wendajilu` 至少一行；
   - `AI_Yitu` 至少一行；
   - 问答表截图字段 `AI_WenTi`、`AI_DaAn`、`AI_Biaozhu`、
     `WenTiYuanWen`、`DaAnYuanWen`、`WenTi_true`、`DaAn_true`、
     `Biaozhu_true` 全部非空；
   - 问答和意图的 `Yssj_id` 与原文 ID 一致。
7. 不删除本次记录，在验证报告中记录文件 SHA256、服务端口、模型名、
   数据库 ID、行数和字段非空布尔值，不记录密钥、密码或完整连接串。

## 完成标准

只有同时满足以下条件才能报告完成：

- 用户指定 PS1 命令成功拉起全部服务。
- Knowledge 后端、WebUI 和代理均 ready。
- 新录音真实转录成功。
- DeepSeek 真实提取成功。
- 三表新记录真实存在并保留。
- 截图字段全部有值。
- 新增程序逐行注释审计为 100%。
- Python、Node、PS1 静态测试和既有回归无失败。
