# Knowledge Management Full-Stack Audio Ingestion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the approved host-process Knowledge Management backend and WebUI start from `start-latest-full-stack.ps1`, then upload `新录音 4.m4a` through the WebUI proxy, transcribe it with SiliconFlow, extract QA/intent records with DeepSeek, and retain correctly mapped rows in all three PostgreSQL tables.

**Architecture:** Docker Compose remains responsible for the existing infrastructure services. A focused `knowledge_api` FastAPI package bootstraps the existing public parsing runtime and extraction runtime, while the existing static WebUI proxies real multipart uploads to it. The extraction persistence layer is corrected against the live PostgreSQL schema and verified column-by-column with a retained end-to-end record set.

**Tech Stack:** Python 3.13, FastAPI, SQLAlchemy 2, pytest, Uvicorn, Node.js built-in test runner, PowerShell 5, FFmpeg, SiliconFlow SenseVoice/DeepSeek-compatible APIs, PostgreSQL.

---

## File structure

- `backend/public_program_files/runtime/app/ai/prompts.py`: common DeepSeek QA output contract; add `answer_completeness`.
- `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/erp_ai_models.py`: align all three ORM models with the live PostgreSQL columns and types.
- `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/raw_data_service.py`: store one complete transcript row and explicitly assign every raw-table field.
- `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/qa_pair_service.py`: map question, standard question, scene, evidence, description, status, time, and reserved/audit fields without collision.
- `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/intent_service.py`: explicitly map every intent-table field.
- `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_database_mapping.py`: isolated field-mapping and long-transcript regression tests.
- `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_extraction_flow.py`: prompt output contract regression test.
- `backend/knowledge_api/__init__.py`: package marker.
- `backend/knowledge_api/runtime_paths.py`: configure DLP-readable runtime paths, `.env` working directory, and Uvicorn dependency path.
- `backend/knowledge_api/response_mapper.py`: parse extraction JSON and map backend results to the WebUI contract.
- `backend/knowledge_api/app.py`: FastAPI app, health route, multipart parse route, and existing VLM router registration.
- `backend/knowledge_api/run_server.py`: executable Uvicorn launcher used by PowerShell.
- `backend/knowledge_api/tests/test_response_mapper.py`: deterministic QA/intent response mapping tests.
- `backend/knowledge_api/tests/test_app.py`: health and multipart route tests with parser/database isolation.
- `webui/src/knowledgeService.mjs`: real FormData upload with long timeout and explicit failures.
- `webui/src/app.mjs`: pass selected upload metadata and display parser failures instead of reporting success.
- `webui/tests/knowledgeService.test.mjs`: multipart/no-mock regression tests.
- `webui/webui_server.py`: preserve multipart headers and allow long proxy requests.
- `webui/tests/test_webui_proxy.py`: proxy timeout and multipart boundary tests.
- `tests/test_full_stack_launcher.py`: static assertions for ports, processes, logs, health checks, and final readiness.
- `tests/test_inline_comment_coverage.py`: include every newly created/modified program file in one-comment-per-code-line auditing.
- `tools/verify_full_stack_audio_ingestion.py`: upload the real audio through port 18321, query all three tables by returned IDs, enforce the field truth table, retain rows, and write a redacted report.
- `app/SQL_RAG/start-latest-full-stack.ps1`: start and health-check Knowledge backend 18320 and WebUI 18321 with the existing services.
- `VERIFICATION_REPORT_2026-07-04.md`: final commands, hashes, ports, models, IDs, row counts, and per-column result booleans; never store secrets.

Every added or changed executable code line receives exactly one adjacent Chinese comment in the same file with one shared implementation timestamp to the second, the line’s purpose, and the reason derived from the approved design/field truth table. Blank lines and comment-only lines are not counted as code lines.

### Task 1: Lock the live schema and field semantics with failing tests

**Files:**
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_database_mapping.py`
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_extraction_flow.py`

- [ ] **Step 1: Replace the old duplicate-field/split expectations with the approved truth table**

Add assertions equivalent to:

```python
analysis = json.dumps([{
    "question": "客户原问题",
    "standard_question": "标准知识问题",
    "answer": "客服答案",
    "question_scene": "采购入库场景",
    "description": "用于检索的问题语义",
    "answer_completeness": "完整",
    "time": "0s-30s",
    "evidence": {
        "customer_text": "问题原文",
        "service_text": "答案原文",
    },
}], ensure_ascii=False)
record = saved_record(analysis)
assert record.AI_WenTi == "客户原问题"
assert record.WenTi_true == "标准知识问题"
assert record.AI_Biaozhu == "采购入库场景"
assert record.Biaozhu_true == "用于检索的问题语义"
assert record.ZhuangTai == 1
assert record.YinPinShiJian == "0s-30s"
assert record.yima is None
```

Change the 2001-character raw-text test to require one record whose `ShuJu` equals the full input and whose `del_time`, `up_userid`, `up_time`, and `yima` are explicitly `None`. Add full intent audit/reserved-field assertions.

- [ ] **Step 2: Add a prompt contract assertion**

Assert that the QA system prompt contains both the JSON key `answer_completeness` and the allowed values `完整/部分完整/不完整/未明确`.

- [ ] **Step 3: Run the focused tests and confirm the expected failures**

Run:

```powershell
& 'ai-ie-backend\app\SQL_RAG\Knowledge_management\.venv\Scripts\python.exe' -m pytest `
  'ai-ie-backend\app\SQL_RAG\Knowledge_management\backend\Extracting_parsed_content_based_on_relevant_prompts\Extraction_of_file_related_prompts\tests\test_database_mapping.py' `
  'ai-ie-backend\app\SQL_RAG\Knowledge_management\backend\Extracting_parsed_content_based_on_relevant_prompts\Extraction_of_file_related_prompts\tests\test_extraction_flow.py' -q
```

Expected: failures show `WenTi_true` still receives `question`, `yima` is absent, long raw text creates two records, and the prompt lacks `answer_completeness`.

- [ ] **Step 4: Commit only the failing tests**

```powershell
git add -- `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_database_mapping.py' `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_extraction_flow.py'
git commit -m 'test: define complete knowledge field mappings'
```

### Task 2: Correct the three-table ORM and persistence mappings

**Files:**
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/public_program_files/runtime/app/ai/prompts.py`
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/erp_ai_models.py`
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/raw_data_service.py`
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/qa_pair_service.py`
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/intent_service.py`

- [ ] **Step 1: Align ORM types and complete the column sets**

Add `yima: Mapped[Optional[str]] = mapped_column("yima", String(64))` to all three models. Match live types: `GuanLianKeHu`, `gs_id`, and both `ZhuangTai_id` columns are strings; `YinPinShiJian` is `String(64)`. Preserve the quoted primary-key names with their embedded spaces.

- [ ] **Step 2: Make the QA prompt emit completeness**

Insert this field into `OUTPUT_FORMAT_PROMPT` after `standard_question`:

```json
"answer_completeness": "完整/部分完整/不完整/未明确",
```

Retain the rule that no information may be invented.

- [ ] **Step 3: Save one complete raw transcript**

Replace the chunk loop with one `ErpYuanShiShuJu` instance:

```python
record = ErpYuanShiShuJu(
    shuju_id=raw_id,
    ZcLeiXin=asset_type_id,
    ShuJu=raw_text,
    WenJianDiZhi=source_file_path,
    WenJianName=source_file_name,
    LaiYuan=_file_type_to_source(file_type),
    GuanLianKeHu=str(guan_lian_ke_hu),
    gs_id=None if enterprise_id is None else str(enterprise_id),
    del_flag=False,
    del_time=None,
    in_userid=None if in_userid is None else str(in_userid),
    in_time=datetime.now(),
    up_userid=None,
    up_time=None,
    yima=None,
)
```

- [ ] **Step 4: Correct QA and intent field assignments**

Use:

```python
AI_WenTi=item.get("question")
WenTi_true=item.get("standard_question") or item.get("question")
AI_Biaozhu=item.get("question_scene")
Biaozhu_true=item.get("description")
ZhuangTai=_status_to_int(item.get("answer_completeness") or item.get("status"))
YinPinShiJian=item.get("time")
yima=None
```

Keep `DaAn_true` equal to `answer` until an explicit human edit exists. Explicitly assign all pending-review/deletion/reserved fields to `None`; do the same for intent `yima`.

- [ ] **Step 5: Run focused and live-schema model tests**

Run the Task 1 command, then a read-only inspector assertion that each ORM column-name set equals the corresponding live table column-name set.

Expected: all focused tests pass and set differences are empty for all three tables.

- [ ] **Step 6: Commit the mapping fix**

```powershell
git add -- `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/public_program_files/runtime/app/ai/prompts.py' `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/erp_ai_models.py' `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/raw_data_service.py' `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/qa_pair_service.py' `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/intent_service.py'
git commit -m 'fix: map every knowledge database field'
```

### Task 3: Build the standalone Knowledge FastAPI service

**Files:**
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/knowledge_api/__init__.py`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/knowledge_api/runtime_paths.py`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/knowledge_api/response_mapper.py`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/knowledge_api/app.py`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/knowledge_api/run_server.py`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/knowledge_api/tests/test_response_mapper.py`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/knowledge_api/tests/test_app.py`

- [ ] **Step 1: Write failing mapper tests**

Use a parser result containing one QA item and one intent item. Require:

```python
assert mapped["fileName"] == "新录音 4.m4a"
assert mapped["fullText"] == "真实转录文本"
assert mapped["rawDataId"] == "raw-id"
assert mapped["qaPairIds"] == ["qa-id"]
assert mapped["intentIds"] == ["intent-id"]
assert mapped["knowledgeItems"][0]["title"] == "标准知识问题"
assert mapped["knowledgeItems"][0]["body"] == "客服答案"
assert mapped["knowledgeItems"][1]["title"] == "咨询操作"
```

- [ ] **Step 2: Write failing API tests**

Patch `process_uploaded_file` with an `AsyncMock`, upload `audio/mp4` through `TestClient`, and assert the route passes `action="analyze"`, `mode="auto"`, `include_parse_result=True`, `asset_type_id`, and `customer_id`. Patch the health probe and require `{"ready": true}` only when key configuration and `SELECT 1` succeed.

- [ ] **Step 3: Run tests and confirm import/route failures**

Run:

```powershell
& 'ai-ie-backend\app\SQL_RAG\Knowledge_management\.venv\Scripts\python.exe' -m pytest `
  'ai-ie-backend\app\SQL_RAG\Knowledge_management\backend\knowledge_api\tests' -q
```

Expected: collection fails because the package/files do not yet exist.

- [ ] **Step 4: Implement runtime bootstrap and response mapping**

`runtime_paths.py` must prepend the extraction and public runtime roots, `chdir` to the public runtime containing `.env`, and add the repository-root virtualenv site-packages only for Uvicorn. `response_mapper.py` must safely parse JSON strings and emit QA plus intent cards without replacing backend failures with mock data.

- [ ] **Step 5: Implement the app and runner**

Create:

```python
app = FastAPI(title="Knowledge Management API")
app.include_router(vlm_router.router)

@app.get("/health")
def health() -> dict[str, object]:
    configured = bool(
        settings.embedding_service_api_key
        and settings.LLM_MODEL
        and settings.AUDIO_TRANSCRIPTION_MODEL
    )
    database_ready = False
    try:
        with sync_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        database_ready = True
    except SQLAlchemyError:
        database_ready = False
    return {
        "ready": configured and database_ready,
        "configured": configured,
        "database": database_ready,
    }

@app.post("/knowledge/parse")
async def parse_knowledge(
    file: UploadFile = File(...),
    asset_type_id: str | None = Form(None),
    customer_id: str = Form("0"),
) -> dict[str, object]:
    if not file.filename:
        raise HTTPException(status_code=400, detail="上传文件名不能为空")
    result = await process_uploaded_file(
        file=file,
        action="analyze",
        mode="auto",
        export_files=False,
        output_dir=None,
        include_parse_result=True,
        asset_type_id=asset_type_id,
        customer_id=int(customer_id),
    )
    if not result.get("success"):
        raise HTTPException(
            status_code=502,
            detail=result.get("error", "文件解析或知识提取失败"),
        )
    return map_process_result(result)
```

`run_server.py` accepts `--host` and `--port`, then calls
`uvicorn.run("knowledge_api.app:app", host=args.host, port=args.port, reload=False)`.

- [ ] **Step 6: Run the API tests**

Expected: all new tests pass.

- [ ] **Step 7: Commit the service**

```powershell
git add -- 'ai-ie-backend/app/SQL_RAG/Knowledge_management/backend/knowledge_api'
git commit -m 'feat: add standalone knowledge ingestion api'
```

### Task 4: Replace mock upload behavior with real multipart transport

**Files:**
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/src/knowledgeService.mjs`
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/src/app.mjs`
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/tests/knowledgeService.test.mjs`

- [ ] **Step 1: Write failing multipart and error tests**

Capture fetch arguments and require `body instanceof FormData`, `body.get("file") === file`, no manually assigned `Content-Type`, and preservation of optional `asset_type_id/customer_id`. Replace the current mock-success test with `await assert.rejects(service.parseUpload(file), /503/)`.

- [ ] **Step 2: Run the Node test and confirm failure**

Run:

```powershell
node --test 'ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/tests/knowledgeService.test.mjs'
```

Expected: current JSON body and mock fallback violate both new tests.

- [ ] **Step 3: Implement real upload/error behavior**

Use a dedicated 10-minute parse timeout:

```javascript
const form = new FormData();
form.append("file", file, file.name);
if (metadata.assetTypeId) form.append("asset_type_id", metadata.assetTypeId);
form.append("customer_id", String(metadata.customerId ?? 0));
return fetchJsonOrThrow(fetchImpl, `${apiBase}/knowledge/parse`, {
  method: "POST",
  body: form,
}, PARSE_TIMEOUT_MS);
```

Keep local fallbacks for state loading/persistence only. In `app.mjs`, wrap parsing in `try/catch`, keep the draft out of the completed state, and display the actual error message.

- [ ] **Step 4: Run all WebUI Node tests**

Run:

```powershell
node --test 'ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/tests/*.test.mjs'
```

Expected: all tests pass.

- [ ] **Step 5: Commit the frontend change**

```powershell
git add -- `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/src/knowledgeService.mjs' `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/src/app.mjs' `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/tests/knowledgeService.test.mjs'
git commit -m 'feat: upload real knowledge files from webui'
```

### Task 5: Make the WebUI proxy safe for long multipart requests

**Files:**
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/webui_server.py`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/tests/test_webui_proxy.py`

- [ ] **Step 1: Write failing proxy tests**

Start a local recording upstream HTTP server, POST a multipart body with a boundary through `KnowledgeWebUIHandler`, and assert byte-for-byte body and `Content-Type` equality. Assert the configured timeout is at least 600 seconds.

- [ ] **Step 2: Run and confirm the timeout failure**

Run:

```powershell
& 'ai-ie-backend\app\SQL_RAG\Knowledge_management\.venv\Scripts\python.exe' -m pytest `
  'ai-ie-backend\app\SQL_RAG\Knowledge_management\webui\tests\test_webui_proxy.py' -q
```

Expected: multipart forwarding passes or exposes a header defect; the current 3-second timeout fails.

- [ ] **Step 3: Implement minimal proxy corrections**

Set `PROXY_TIMEOUT_SECONDS = 600`, forward the original content type including its multipart boundary, preserve upstream error bodies, and continue returning explicit 502/500 JSON on connection failures.

- [ ] **Step 4: Re-run proxy and Node tests**

Expected: all pass.

- [ ] **Step 5: Commit the proxy**

```powershell
git add -- `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/webui_server.py' `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/tests/test_webui_proxy.py'
git commit -m 'fix: proxy long knowledge multipart uploads'
```

### Task 6: Integrate both Knowledge services into the full-stack PowerShell launcher

**Files:**
- Modify: `ai-ie-backend/app/SQL_RAG/start-latest-full-stack.ps1`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_full_stack_launcher.py`

- [ ] **Step 1: Write a failing static launcher test**

Require the script to contain:

```text
KnowledgeBackendPort=18320
KnowledgeWebPort=18321
backend\knowledge_api\run_server.py
Knowledge_management\webui\webui_server.py
/health
/api/health
knowledge-backend-
knowledge-webui-
knowledgeBackendReady
knowledgeWebReady
knowledgeProxyReady
```

Also assert the final all-ready predicate contains all three Knowledge readiness flags and `Stop-SqlRagPythonApps` includes both process signatures.

- [ ] **Step 2: Run and confirm failure**

Run:

```powershell
& 'ai-ie-backend\app\SQL_RAG\Knowledge_management\.venv\Scripts\python.exe' -m pytest `
  'ai-ie-backend\app\SQL_RAG\Knowledge_management\tests\test_full_stack_launcher.py' -q
```

Expected: the current script has no Knowledge service integration.

- [ ] **Step 3: Extend the existing script without overwriting unrelated edits**

Add the two default ports/URLs, port cleanup and fallback recomputation, process cleanup signatures, four log paths, two hidden `Start-Process` calls, direct/proxy health checks, address/log output, and readiness flags. Launch the backend with the Knowledge `.venv` Python and `backend\knowledge_api\run_server.py`; launch the WebUI with the same Python and `--backend-url`.

- [ ] **Step 4: Parse-check and run the static test**

Run:

```powershell
[scriptblock]::Create((Get-Content -LiteralPath 'ai-ie-backend\app\SQL_RAG\start-latest-full-stack.ps1' -Raw)) | Out-Null
& 'ai-ie-backend\app\SQL_RAG\Knowledge_management\.venv\Scripts\python.exe' -m pytest `
  'ai-ie-backend\app\SQL_RAG\Knowledge_management\tests\test_full_stack_launcher.py' -q
```

Expected: PowerShell parsing succeeds and the test passes.

- [ ] **Step 5: Commit only the task-specific hunk and test**

Review `git diff` carefully because the PS1 already contains unrelated user changes. Stage the test normally and stage only the Knowledge integration hunk from the PS1.

### Task 7: Add the retained end-to-end verifier and comment audit

**Files:**
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tools/verify_full_stack_audio_ingestion.py`
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_inline_comment_coverage.py`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_verifier_contract.py`

- [ ] **Step 1: Write failing verifier-contract tests**

Require the verifier to:

- calculate SHA256;
- upload through `http://127.0.0.1:18321/api/knowledge/parse`;
- require nonempty `raw_data_id`, `qa_pair_ids`, and `intent_ids`;
- reflect live table columns and compare them to ORM columns;
- validate every field using the approved null/non-null/value rules;
- write only model names, IDs, counts, lengths, booleans, ports, and hash;
- never delete rows and never serialize keys/passwords/connection strings.

- [ ] **Step 2: Implement the verifier**

Use `urllib.request` or `httpx` multipart upload and SQLAlchemy reflected tables. Select a real `AI_ZiChanLeiXing.zclxId`, pass it as `asset_type_id`, pass an explicit test `customer_id`, record the test start time, then query by returned IDs and enforce all three field truth tables. Exit nonzero on any mismatch.

- [ ] **Step 3: Extend one-comment-per-code-line coverage**

Add every Python, JavaScript, and PowerShell program file modified or created by Tasks 1–7,
including test programs, to the audit. Require one adjacent Chinese explanation per executable
line and a timestamp matching `YYYY-MM-DD HH:MM:SS`; reject consecutive comments for one
code line, orphan comments, and uncovered code.

- [ ] **Step 4: Run verifier-contract and comment-coverage tests**

Expected: both pass before any live external call.

- [ ] **Step 5: Commit verifier and audits**

```powershell
git add -- `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/tools/verify_full_stack_audio_ingestion.py' `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_inline_comment_coverage.py' `
  'ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_verifier_contract.py'
git commit -m 'test: verify retained knowledge ingestion rows'
```

### Task 8: Run all automated regression tests

**Files:**
- No new files.

- [ ] **Step 1: Compile all Python**

Run `compileall` over `Knowledge_management/backend`, `Knowledge_management/tools`, and `Knowledge_management/webui`.

Expected: exit code 0.

- [ ] **Step 2: Run all Knowledge Python tests except explicitly live tests**

Run the top-level, parsing-chain, extraction-chain, knowledge API, and WebUI proxy suites with the Knowledge `.venv`; exclude tests marked live.

Expected: zero failures.

- [ ] **Step 3: Run all Node tests**

Run:

```powershell
node --test 'ai-ie-backend/app/SQL_RAG/Knowledge_management/webui/tests/*.test.mjs'
```

Expected: zero failures.

- [ ] **Step 4: Run comment, schema, and duplicate-source audits**

Require 100% line-comment coverage, exact ORM/live-schema equality, and no duplicate common runtime files reintroduced into either business chain.

Expected: all audits pass.

### Task 9: Execute the exact full-stack command and retain real database rows

**Files:**
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/VERIFICATION_REPORT_2026-07-04.md`

- [ ] **Step 1: Record pre-test table state**

Read-only query the three row counts and capture the current maximum `in_time`. Do not output credentials.

- [ ] **Step 2: Start the exact user command**

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
& 'D:\wkt\ai-ie-backend-feature-rag-new (1)\ai-ie-backend\app\SQL_RAG\start-latest-full-stack.ps1'
```

Expected: Docker dependencies and all six host services are ready; Knowledge URLs are exactly 18320/18321 unless the script explicitly reports a verified fallback.

- [ ] **Step 3: Verify direct and proxy health**

Require HTTP 200 and `ready=true` from `18320/health`, HTTP 200 from `18321/health`, and `ready=true` from `18321/api/health`.

- [ ] **Step 4: Run the real retained ingestion**

Invoke the verifier against:

```text
D:\wkt\ai-ie-backend-feature-rag-new (1)\ai-ie-backend\新录音 4.m4a
```

Expected: SiliconFlow returns nonempty transcription; DeepSeek returns at least one QA and one intent; all returned database IDs are nonempty.

- [ ] **Step 5: Query all retained rows and verify the field truth table**

Require:

- the `AI_YuanShishuju` row contains the full nonempty transcript, correct filename, `LaiYuan=3`, selected asset ID, customer ID, active/audit/reserved values;
- every `AI_Wendajilu` row contains nonempty question, answer, scene, both evidence texts, standard question, description, time, valid status, and correct null metadata;
- every `AI_Yitu` row contains nonempty intent, description, evidence, time, status 0, and correct null metadata;
- every child `Yssj_id` equals the returned `raw_data_id`;
- post-test row counts increased by exactly the returned row counts;
- no cleanup SQL is executed（本次新记录不清理）.

- [ ] **Step 6: Write the redacted verification report**

Include timestamp, audio SHA256/size, actual ports, configured model names, health booleans, IDs, row-count deltas, and per-field booleans. Exclude transcript contents, API keys, database passwords, and full connection strings.

- [ ] **Step 7: Run completion verification**

Re-run the automated test commands from Task 8 after the live test and inspect all Knowledge logs for traceback/error markers.

Expected: tests still pass, logs contain no unhandled errors, and retained rows remain queryable.

- [ ] **Step 8: Commit only task-owned implementation/report files**

Review the dirty worktree, avoid staging unrelated existing changes, and commit the final report plus any uncommitted task-owned hunks.
