# Dynamic Asset Prompt Knowledge Flow Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make company and asset CRUD drive a strict database-backed three-step DeepSeek prompt flow, then prove the real UI-to-database path with a retained asset, retained prompts, a real audio upload, and field-level verification.

**Architecture:** PostgreSQL remains the only contract between Asset Type Management and Knowledge Management. The asset row selects a prompt group by `(gsId, zclxId)`, the prompt repository resolves active rows by `(gsId, tscId, Tishicileixing)`, and the extraction chain refuses to run unless all three database prompt types are present. Output JSON schemas remain code-owned contracts, while every business instruction is selected dynamically from the database.

**Tech Stack:** Python 3, FastAPI, psycopg 3, SQLAlchemy, vanilla JavaScript ES modules, Node test runner, PostgreSQL, SiliconFlow OpenAI-compatible DeepSeek API, PowerShell, local browser automation.

---

## File Structure

- Modify `app/SQL_RAG/Asset_type_management/webui/index.html`: add editable company/gsId field to the asset CRUD modal.
- Modify `app/SQL_RAG/Asset_type_management/webui/src/assetStore.mjs`: persist `companyId` in browser state.
- Modify `app/SQL_RAG/Asset_type_management/webui/src/app.mjs`: bind the company field to create/edit operations.
- Modify `app/SQL_RAG/Asset_type_management/Data_storage_logic/mian_Asset_type_logic/asset_type_repository.py`: propagate each asset company ID into its prompt rows instead of using a global default.
- Modify Asset Type Management tests: lock company-aware CRUD and prompt persistence.
- Modify `app/SQL_RAG/Knowledge_management/backend/knowledge_api/prompt_repository.py`: implement strict composite selection, ordered same-type merging, database-only sources, and screenshot titles.
- Modify `app/SQL_RAG/Knowledge_management/backend/knowledge_api/app.py`: require both asset ID and gsId before resolving or executing prompts.
- Create `app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/output_contracts.py`: own only JSON shape contracts, not business instructions.
- Modify `audio_knowledge_extract_service.py`: require three dynamic prompts and remove business-prompt constant fallbacks.
- Modify Knowledge Management backend tests: lock strict prompt selection, output contracts, API rejection, and result titles.
- Modify `app/SQL_RAG/Knowledge_management/webui/src/knowledgeStore.mjs`: clear stale prompt bundles and expose a strict readiness check.
- Modify `app/SQL_RAG/Knowledge_management/webui/src/app.mjs`: block file selection/upload until the selected company and asset resolve three database prompt types.
- Modify Knowledge Management WebUI tests: lock the readiness gate and screenshot title display.
- Modify `app/SQL_RAG/Knowledge_management/tools/verify_full_stack_audio_ingestion.py`: verify the retained asset, three prompt rows, original row, QA rows, intent rows, prompt hashes, associations, and response titles.
- Modify comment audit tests only when a newly executable file must be added to the audited ownership list.

### Task 1: Make asset and prompt CRUD company-aware

**Files:**
- Modify: `app/SQL_RAG/Asset_type_management/Data_storage_logic/mian_Asset_type_logic/test_asset_type_repository.py`
- Modify: `app/SQL_RAG/Asset_type_management/Data_storage_logic/mian_Asset_type_logic/test_asset_type_mapping.py`
- Modify: `app/SQL_RAG/Asset_type_management/Data_storage_logic/mian_Asset_type_logic/asset_type_repository.py`
- Modify: `app/SQL_RAG/Asset_type_management/webui/tests/assetStore.test.mjs`
- Modify: `app/SQL_RAG/Asset_type_management/webui/tests/modalSwitching.test.mjs`
- Modify: `app/SQL_RAG/Asset_type_management/webui/src/assetStore.mjs`
- Modify: `app/SQL_RAG/Asset_type_management/webui/src/app.mjs`
- Modify: `app/SQL_RAG/Asset_type_management/webui/index.html`

- [ ] **Step 1: Write failing repository tests for company propagation**

Add assertions equivalent to:

```python
record = prompt_payload_to_record(
    prompt_group_id="asset-company-a",
    company_id="QY90001",
    category="qa",
    prompt={"content": "公司 A 问答提示词"},
    order_index=1,
    now=datetime(2026, 7, 6, 12, 0, 0),
)
assert record["gsId"] == "QY90001"
```

Add a persistence-mapping test that proves `_persist_prompt_bucket` receives the company ID from the same asset record rather than `DEFAULT_COMPANY_ID`.

- [ ] **Step 2: Write failing WebUI tests for editable company ID**

Extend `assetStore.test.mjs` so a new asset saved with `companyId: "QY90001"` keeps that value through create and edit. Extend `modalSwitching.test.mjs` to assert `index.html` contains `id="companyId"` and `app.mjs` reads/writes `dom.companyId`.

- [ ] **Step 3: Run the focused tests and verify RED**

Run:

```powershell
python -m unittest app.SQL_RAG.Asset_type_management.Data_storage_logic.mian_Asset_type_logic.test_asset_type_repository app.SQL_RAG.Asset_type_management.Data_storage_logic.mian_Asset_type_logic.test_asset_type_mapping -v
node --test app/SQL_RAG/Asset_type_management/webui/tests/assetStore.test.mjs app/SQL_RAG/Asset_type_management/webui/tests/modalSwitching.test.mjs
```

Expected: repository tests fail because `prompt_payload_to_record` has no `company_id` parameter; WebUI tests fail because the company field is absent.

- [ ] **Step 4: Implement company-aware asset CRUD**

Change the prompt mapper signature to:

```python
def prompt_payload_to_record(
    prompt_group_id: str,
    company_id: str,
    category: str,
    prompt: dict[str, Any],
    order_index: int,
    now: datetime,
) -> dict[str, Any]:
```

Write `"gsId": str(company_id).strip()` and reject an empty company ID. In `persist_state`, keep `{record["zclxId"]: {"prompt_group_id": record["tscId"], "company_id": record["gsId"]}}` and pass both values into `_persist_prompt_bucket`. Add the exact HTML element `<input id="companyId" type="text" placeholder="请输入公司ID/gsId">`, bind it in `app.mjs`, and normalize it in `assetStore.mjs`; the test asset uses `QY20001` but the field supports any non-empty company ID.

Every new executable line receives an adjacent comment such as `[2026-07-06 12:00:00] 作用：保存资产所属公司ID；理由依据：提示词选择必须同时匹配公司和资产。`.

- [ ] **Step 5: Run the focused tests and verify GREEN**

Run the Step 3 commands. Expected: all focused tests pass.

### Task 2: Implement strict dynamic prompt selection

**Files:**
- Modify: `app/SQL_RAG/Knowledge_management/backend/knowledge_api/tests/test_prompt_repository.py`
- Modify: `app/SQL_RAG/Knowledge_management/backend/knowledge_api/prompt_repository.py`

- [ ] **Step 1: Write failing tests for the strict bundle contract**

Add tests with one asset and prompt rows that assert:

```python
bundle = build_prompt_bundle(
    {"zclxId": "asset-a", "gsId": "QY90001", "tscId": "group-a", "ziChanLeiXing": "公司 A 客服"},
    [
        {"Tishicileixing": 1, "tiShiCiBianMa": "qa-2", "yima": "2", "prompt": "QA-B"},
        {"Tishicileixing": 1, "tiShiCiBianMa": "qa-1", "yima": "1", "prompt": "QA-A"},
        {"Tishicileixing": 2, "tiShiCiBianMa": "intent-1", "yima": "1", "prompt": "INTENT"},
        {"Tishicileixing": 3, "tiShiCiBianMa": "decompose-1", "yima": "1", "prompt": "DECOMPOSE"},
    ],
    "QY90001",
)
assert bundle["promptOverrides"]["qa"] == "QA-A\n\nQA-B"
assert [item["source"] for item in bundle["promptBlocks"]] == ["database"] * 3
assert [item["title"] for item in bundle["promptBlocks"]] == ["知识标注提示词", "意图发现提示词", "意图发现AI提取"]
assert bundle["promptBlocks"][0]["promptCodes"] == ["qa-1", "qa-2"]
```

Add parameterized failures for missing `asset_type_id`, missing `gs_id`, company mismatch, missing type 1/2/3, unknown type code, and empty prompt content.

- [ ] **Step 2: Run prompt repository tests and verify RED**

Run:

```powershell
app/SQL_RAG/Knowledge_management/.venv/Scripts/python.exe -m pytest --import-mode=importlib app/SQL_RAG/Knowledge_management/backend/knowledge_api/tests/test_prompt_repository.py -q
```

Expected: failures show fallback sources, old titles, first-row-only behavior, and missing strict validation.

- [ ] **Step 3: Replace fallback selection with strict grouping**

Remove imports of `QA_EXTRACTION_PROMPT`, `DESCRIPTION_PROMPT`, and `YT_PROMPT` from `prompt_repository.py`. Remove `PROMPT_FALLBACK_CONTENT`. Implement these rules:

```python
PROMPT_ORDER = ("qa", "intent", "decompose")
PROMPT_JOIN_SEPARATOR = "\n\n"

def build_prompt_bundle(asset: dict, prompt_rows: list[dict], gs_id: str) -> dict:
    # validate asset ID, exact company match and prompt group
    # reject unknown types and empty active prompt text
    # sort each type by numeric yima, in_time, tiShiCiBianMa
    # require every PROMPT_ORDER key
    # join every active row of the same type
    # return source="database" and promptCodes for every block
```

Update `resolve_asset_prompt_bundle` so its asset SQL includes exact `"gsId" = :gs_id` and active state, and its prompt SQL includes exact `"gsId" = :gs_id`, `COALESCE("TiShiCiZhuangTai", 1) = 1`, and `COALESCE("del_flag", false) = false`. Delete the broad fallback query that ignores company ID.

- [ ] **Step 4: Run prompt repository tests and verify GREEN**

Run the Step 2 command. Expected: all prompt repository tests pass.

### Task 3: Remove hard-coded business prompt fallbacks from extraction

**Files:**
- Create: `app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/output_contracts.py`
- Modify: `app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/runtime/extraction_chain/audio_knowledge_extract_service.py`
- Modify: `app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_extraction_flow.py`

- [ ] **Step 1: Write failing extraction tests**

Add tests that assert `extract_audio_knowledge("原文", {})` raises `ValueError` listing `qa, intent, decompose`, and that captured system prompts contain supplied database text:

```python
prompts = {"qa": "DB-QA", "intent": "DB-INTENT", "decompose": "DB-DECOMPOSE"}
await extract_audio_knowledge("客户问怎么操作", prompt_overrides=prompts)
assert captured_system_prompts[0].startswith("DB-QA")
assert captured_system_prompts[1].startswith("DB-DECOMPOSE")
assert captured_system_prompts[2].startswith("DB-INTENT")
assert "企业软件服务知识库整理专家" not in captured_system_prompts[0]
```

The tests must also prove each system prompt ends with the required JSON field contract.

- [ ] **Step 2: Run extraction tests and verify RED**

Run:

```powershell
app/SQL_RAG/Knowledge_management/.venv/Scripts/python.exe -m pytest --import-mode=importlib app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_extraction_flow.py -q
```

Expected: empty overrides currently fall back to business constants and intent appends the full `YT_PROMPT`.

- [ ] **Step 3: Add code-owned output contracts and require database prompts**

Create `output_contracts.py` with `QA_JSON_OUTPUT_CONTRACT`, `DESCRIPTION_JSON_OUTPUT_CONTRACT`, and `INTENT_JSON_OUTPUT_CONTRACT`. Each constant contains only field names and JSON shape, never domain/business instructions.

Delete `_select_prompt` and replace every call site with the following strict validator:

```python
REQUIRED_DYNAMIC_PROMPTS = ("qa", "intent", "decompose")

def require_dynamic_prompts(prompt_overrides: dict[str, str] | None) -> dict[str, str]:
    normalized = {key: str((prompt_overrides or {}).get(key) or "").strip() for key in REQUIRED_DYNAMIC_PROMPTS}
    missing = [key for key, value in normalized.items() if not value]
    if missing:
        raise ValueError(f"缺少数据库动态提示词：{', '.join(missing)}")
    return normalized
```

Pass the validated dictionary through all three extraction calls. Append only the matching JSON output contract and the retry contract. Remove imports of `QA_EXTRACTION_PROMPT`, `DESCRIPTION_PROMPT`, `YT_PROMPT`, and `OUTPUT_FORMAT_PROMPT` from this service.

- [ ] **Step 4: Run extraction tests and verify GREEN**

Run the Step 2 command. Expected: all extraction tests pass and captured prompts use database business content only.

### Task 4: Enforce strict context in Knowledge API and WebUI

**Files:**
- Modify: `app/SQL_RAG/Knowledge_management/backend/knowledge_api/tests/test_app.py`
- Modify: `app/SQL_RAG/Knowledge_management/backend/knowledge_api/app.py`
- Modify: `app/SQL_RAG/Knowledge_management/webui/tests/knowledgeStore.test.mjs`
- Modify: `app/SQL_RAG/Knowledge_management/webui/tests/addPageLayout.test.mjs`
- Modify: `app/SQL_RAG/Knowledge_management/webui/tests/knowledgeService.test.mjs`
- Modify: `app/SQL_RAG/Knowledge_management/webui/src/knowledgeStore.mjs`
- Modify: `app/SQL_RAG/Knowledge_management/webui/src/app.mjs`

- [ ] **Step 1: Write failing API and browser-state tests**

Backend tests assert `/knowledge/prompts` and `/knowledge/parse` reject missing `asset_type_id` or `gs_id`, and that `process_uploaded_file` is not called after prompt configuration failure.

Node tests add:

```javascript
assert.equal(isPromptBundleReady(null, "asset-a", "QY90001"), false);
assert.equal(isPromptBundleReady({
  assetTypeId: "asset-a",
  gsId: "QY90001",
  promptBlocks: [
    { promptType: "qa", source: "database", content: "QA" },
    { promptType: "intent", source: "database", content: "INTENT" },
    { promptType: "decompose", source: "database", content: "DECOMPOSE" },
  ],
}, "asset-a", "QY90001"), true);
```

Also assert changing `assetTypeId` or `customerId` clears `addDraft.promptBundle` so stale prompts cannot authorize upload.

- [ ] **Step 2: Run focused tests and verify RED**

Run:

```powershell
app/SQL_RAG/Knowledge_management/.venv/Scripts/python.exe -m pytest --import-mode=importlib app/SQL_RAG/Knowledge_management/backend/knowledge_api/tests/test_app.py -q
node --test app/SQL_RAG/Knowledge_management/webui/tests/knowledgeStore.test.mjs app/SQL_RAG/Knowledge_management/webui/tests/addPageLayout.test.mjs app/SQL_RAG/Knowledge_management/webui/tests/knowledgeService.test.mjs
```

Expected: the API still accepts legacy missing context and the WebUI has no strict readiness function.

- [ ] **Step 3: Implement API strictness and upload gating**

Make `asset_type_id` and `gs_id` required form/query values for the live Knowledge routes. Convert prompt-resolution `ValueError` to HTTP 400 without calling the extraction chain.

Export `isPromptBundleReady` from `knowledgeStore.mjs`. It must require exact asset ID, exact gsId, exactly the three prompt types, `source === "database"`, and non-empty content. Clear `promptBundle` whenever asset or customer context changes. In `parseSelectedFile`, refresh the bundle first, verify readiness, then attach the file and call `parseUpload`; on failure return to idle and display the exact error. Render the upload control disabled with an explanatory message until readiness is true.

- [ ] **Step 4: Run focused tests and verify GREEN**

Run the Step 2 commands. Expected: all focused API and Node tests pass.

### Task 5: Align result titles and response evidence

**Files:**
- Modify: `app/SQL_RAG/Knowledge_management/backend/knowledge_api/tests/test_response_mapper.py`
- Modify: `app/SQL_RAG/Knowledge_management/backend/knowledge_api/tests/test_prompt_repository.py`
- Modify: `app/SQL_RAG/Knowledge_management/backend/knowledge_api/response_mapper.py` only if normalization is required after strict prompt blocks are returned.
- Modify: `app/SQL_RAG/Knowledge_management/webui/tests/addPageLayout.test.mjs`

- [ ] **Step 1: Write failing title and evidence tests**

Assert the response contains titles in this order: `知识标注提示词`, `意图发现提示词`, `意图发现AI提取`. Assert every block retains `promptType`, `source`, `promptCodes`, and full content. Assert each knowledge card maps non-empty `marker` and `body` from the corresponding QA/intent fields.

- [ ] **Step 2: Run tests and verify RED**

Run:

```powershell
app/SQL_RAG/Knowledge_management/.venv/Scripts/python.exe -m pytest --import-mode=importlib app/SQL_RAG/Knowledge_management/backend/knowledge_api/tests/test_response_mapper.py app/SQL_RAG/Knowledge_management/backend/knowledge_api/tests/test_prompt_repository.py -q
```

Expected: old titles or dropped block metadata fail assertions.

- [ ] **Step 3: Preserve strict prompt block metadata in the response**

Update `_build_analysis_blocks` so it copies `promptType`, `source`, `promptCodes`, `promptGroupId`, title, icon, and content from the strict bundle. Do not synthesize fallback blocks on the live upload path.

- [ ] **Step 4: Run tests and verify GREEN**

Run the Step 2 command. Expected: response mapping tests pass.

### Task 6: Extend the retained-data verifier

**Files:**
- Modify: `app/SQL_RAG/Knowledge_management/tests/test_verifier_contract.py`
- Modify: `app/SQL_RAG/Knowledge_management/tools/verify_full_stack_audio_ingestion.py`

- [ ] **Step 1: Write failing verifier contract tests**

Assert the verifier requires `--asset-type-id` and `--gs-id`, calls `http://127.0.0.1:18321/api/knowledge/prompts` before upload, rejects non-database prompt sources, records the three prompt SHA-256 values, and queries all five involved tables by the generated IDs.

- [ ] **Step 2: Run verifier contract tests and verify RED**

Run:

```powershell
app/SQL_RAG/Knowledge_management/.venv/Scripts/python.exe -m pytest --import-mode=importlib app/SQL_RAG/Knowledge_management/tests/test_verifier_contract.py -q
```

Expected: current report lacks retained asset/prompt evidence and strict source checks.

- [ ] **Step 3: Implement field-level verification**

The report must include:

```python
{
    "asset": {"zclxId": asset_id, "gsId": args.gs_id, "tscId": prompt_group_id, "name": asset_name},
    "prompts": [{"code": prompt_code, "type": prompt_type, "sha256": prompt_sha256, "source": "database"}],
    "raw": {"id": payload["rawDataId"], "assetTypeId": asset_id, "gsId": args.gs_id, "textLength": len(payload["fullText"])},
    "qa": {"ids": payload["qaPairIds"], "count": len(payload["qaPairIds"]), "requiredFieldsNonEmpty": qa_fields_ok},
    "intent": {"ids": payload["intentIds"], "count": len(payload["intentIds"]), "requiredFieldsNonEmpty": intent_fields_ok},
    "responseTitles": ["知识标注提示词", "意图发现提示词", "意图发现AI提取"],
}
```

Abort with non-zero exit when a prompt is fallback, a relationship differs, a required result field is empty, or QA/intent output is empty.

- [ ] **Step 4: Run verifier contract tests and verify GREEN**

Run the Step 2 command. Expected: all verifier contract tests pass.

### Task 7: Run complete automated verification and comment audit

**Files:**
- Modify: `app/SQL_RAG/Knowledge_management/tests/test_new_program_comment_coverage.py` only if `output_contracts.py` is not automatically discovered.
- Verify all changed files.

- [ ] **Step 1: Run Python backend suites**

Run:

```powershell
python -m unittest discover -s app/SQL_RAG/Asset_type_management/Data_storage_logic/mian_Asset_type_logic -p 'test_*.py' -v
app/SQL_RAG/Knowledge_management/.venv/Scripts/python.exe -m pytest --import-mode=importlib app/SQL_RAG/Knowledge_management/backend/knowledge_api/tests app/SQL_RAG/Knowledge_management/backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_extraction_flow.py app/SQL_RAG/Knowledge_management/tests/test_verifier_contract.py -q
```

Expected: zero failures.

- [ ] **Step 2: Run both WebUI suites**

Run:

```powershell
node --test app/SQL_RAG/Asset_type_management/webui/tests/*.test.mjs
node --test app/SQL_RAG/Knowledge_management/webui/tests/*.test.mjs
```

Expected: zero failures.

- [ ] **Step 3: Run syntax and comment audits**

Run:

```powershell
app/SQL_RAG/Knowledge_management/.venv/Scripts/python.exe -m compileall -q app/SQL_RAG/Asset_type_management app/SQL_RAG/Knowledge_management
node --check app/SQL_RAG/Asset_type_management/webui/src/app.mjs
node --check app/SQL_RAG/Asset_type_management/webui/src/assetStore.mjs
node --check app/SQL_RAG/Knowledge_management/webui/src/app.mjs
node --check app/SQL_RAG/Knowledge_management/webui/src/knowledgeStore.mjs
app/SQL_RAG/Knowledge_management/.venv/Scripts/python.exe -m pytest --import-mode=importlib app/SQL_RAG/Knowledge_management/tests/test_new_program_comment_coverage.py -q
```

Expected: syntax exit code 0 and comment audit zero missing lines.

### Task 8: Create retained data through the real Asset Type UI

**Files:**
- No production-code change expected.
- Evidence output uses `$runStamp = Get-Date -Format 'yyyyMMdd_HHmmss'` and `app/SQL_RAG/Knowledge_management/backend/knowledge_api/manifests/dynamic_prompt_asset_$runStamp.json`.

- [ ] **Step 1: Restart the latest full stack**

Run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force
& 'D:\wkt\ai-ie-backend-feature-rag-new (1)\ai-ie-backend\app\SQL_RAG\start-latest-full-stack.ps1'
```

Expected: Asset backend/WebUI and Knowledge backend/WebUI all report ready on their printed ports.

- [ ] **Step 2: Use the real Asset Type Management UI**

Open `http://127.0.0.1:18191/`. Create `知识库三步动态提示词联调-20260706-HHmmss`, set company ID `QY20001`, preserve it permanently, and save the asset. Enter the prompt editor and save:

- Type 1: exact `QA_EXTRACTION_PROMPT` business text.
- Type 2: exact `YT_PROMPT` business text.
- Type 3: exact `DESCRIPTION_PROMPT` business text.

Read back the asset state from the live API and record the generated asset ID and prompt codes. Assert the three stored text SHA-256 values match the source constants.

- [ ] **Step 3: Verify strict prompt preview before upload**

Store the generated browser/API asset ID in `$assetId`, then call `/api/knowledge/prompts?asset_type_id=$assetId&gs_id=QY20001` through port 18321. Assert exact company/asset IDs, three database sources, expected titles, expected prompt codes, and exact hashes.

### Task 9: Run the real Knowledge UI upload and precise database verification

**Files:**
- Evidence output uses the same `$runStamp` and `app/SQL_RAG/Knowledge_management/backend/knowledge_api/manifests/dynamic_prompt_e2e_$runStamp.json`.

- [ ] **Step 1: Use the Knowledge Management UI**

Open `http://127.0.0.1:18321/`, enter 新增知识, select the retained asset and `QY20001`, confirm upload becomes enabled, then drag or select `D:\wkt\ai-ie-backend-feature-rag-new (1)\ai-ie-backend\新录音 4.m4a`.

Expected UI states: parsing indicator, original content, three approved titles with database prompt content, and non-empty red knowledge extraction cards.

- [ ] **Step 2: Run the strict verifier against the same retained asset**

Run:

```powershell
$runStamp = Get-Date -Format 'yyyyMMdd_HHmmss'
app/SQL_RAG/Knowledge_management/.venv/Scripts/python.exe app/SQL_RAG/Knowledge_management/tools/verify_full_stack_audio_ingestion.py --audio 'D:\wkt\ai-ie-backend-feature-rag-new (1)\ai-ie-backend\新录音 4.m4a' --asset-type-id $assetId --customer-id 0 --gs-id QY20001 --endpoint http://127.0.0.1:18321/api/knowledge/parse --report "app/SQL_RAG/Knowledge_management/backend/knowledge_api/manifests/dynamic_prompt_e2e_$runStamp.json"
```

Expected: exit code 0; one new original row; at least one new QA row; at least one new intent row; all required fields and foreign-key-like associations verified.

- [ ] **Step 3: Recheck health after live calls**

Verify Asset backend/WebUI and Knowledge backend/WebUI return HTTP 200 and ready status. Read recent service logs and require no `Traceback`, unhandled `ERROR`, or silent fallback markers.

### Task 10: Final evidence review

**Files:**
- Review the design spec, this plan, git diff, retained-data manifest, and service logs.

- [ ] **Step 1: Compare implementation against every design completion condition**

Confirm all seven conditions in `docs/superpowers/specs/2026-07-06-dynamic-asset-prompt-knowledge-flow-design.md` Section 8 have direct evidence.

- [ ] **Step 2: Review the diff for unintended files and secrets**

Run `git diff --check` and inspect only files touched by this implementation. Do not stage or modify unrelated existing work. Confirm no API key, password, or full connection string appears in reports.

- [ ] **Step 3: Report only freshly verified results**

Report service URLs, retained asset ID, prompt codes and types, prompt-source checks, `rawDataId`, QA IDs, intent IDs, exact test counts, comment-audit result, and manifest paths. If any condition fails, report the failure and continue work instead of claiming completion.
