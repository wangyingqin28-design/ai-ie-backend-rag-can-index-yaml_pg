# File Parsing and DeepSeek Extraction Migration Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Recover and test the two source execution chains, then create two independently runnable, fully inventoried and line-annotated mirrors under the requested SQL_RAG Knowledge_management directories.

**Architecture:** Each destination contains a private `runtime/app` mirror so original `app.*` imports and module boundaries remain intact. Tests run each mirror in a subprocess with that mirror first on `PYTHONPATH`; source credentials are copied only to ignored runtime `.env` files, while tracked `.env.example` files contain names but no secrets. Static AST manifests, runtime traces, hashes and one-to-one physical-line annotation ledgers prove completeness.

**Tech Stack:** Python 3.13, pytest, FastAPI UploadFile, OpenAI-compatible SiliconFlow API, SQLAlchemy/PostgreSQL, Docling, LlamaIndex, Qdrant Client, PowerShell, Git.

---

### Task 1: Establish source recovery and completeness tests

**Files:**
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_source_chain_recovery.py`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tools/chain_inventory.py`
- Test: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_source_chain_recovery.py`

- [ ] **Step 1: Write the failing UTF-8 and AST test**

```python
def test_all_source_chain_modules_are_utf8_and_parseable(source_modules):
    failures = []
    for path in source_modules:
        try:
            ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
        except (UnicodeDecodeError, SyntaxError) as exc:
            failures.append((str(path), str(exc)))
    assert failures == []
```

- [ ] **Step 2: Run the test and capture the expected RED result**

Run: `pytest -q ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_source_chain_recovery.py`

Expected: FAIL naming `app/ai/processors/document_service.py` and the truncated UTF-8 sequence near byte 1545.

- [ ] **Step 3: Implement a read-only AST inventory tool**

The tool indexes source modules, follows absolute imports, relative imports and imports nested inside functions, substitutes the explicitly recorded recovery reference only while reporting the damaged module, and writes no files unless an output path is supplied. Its public API is `collect_module_closure(source_root, seeds) -> dict[str, Path]` and `collect_definitions(modules) -> list[Definition]`; `Definition` is a frozen dataclass containing `module`, `qualname`, `kind`, `lineno`, and `end_lineno`. Import resolution must use the importing module's package and `ImportFrom.level`, and definition qualification must be built by an AST visitor stack so class methods are emitted as `ClassName.method_name`.

- [ ] **Step 4: Record the damaged bytes before repair**

Run: `Get-FileHash -Algorithm SHA256 <source-document-service>; Format-Hex <source-document-service> | Select-Object -Last 12`

Expected: a SHA256 value and a tail ending with the incomplete UTF-8 bytes already observed.

### Task 2: Recover the truncated document parser using TDD

**Files:**
- Create: `D:/wkt/getsoft---ai-erp-backend-feature-rag-new/getsoft---ai-erp-backend/app/ai/processors/document_service.py.corrupt-20260703.bak`
- Modify: `D:/wkt/getsoft---ai-erp-backend-feature-rag-new/getsoft---ai-erp-backend/app/ai/processors/document_service.py`
- Test: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_source_chain_recovery.py`

- [ ] **Step 1: Preserve the exact damaged bytes**

Copy the file byte-for-byte to the named backup, then assert source and backup SHA256 values match before changing the source.

- [ ] **Step 2: Restore the minimal complete implementation**

Use the intact homologous `ai-ie-backend/app/ai/vlmLI/document_service.py` as evidence. Preserve the valid source prefix through `_safe_export_to_dict`, then restore reference lines 24-132 beginning at `build_docling_converter`. Do not copy the reference's unused `from .llm_client import llm_model_func` import. The final AST must contain exactly `_safe_export_to_markdown`, `_safe_export_to_dict`, `build_docling_converter`, `parse_document_with_docling`, `process_document_file`, `query_document_with_llamaindex`, and `process_text_file`, with signatures identical to the reference.

- [ ] **Step 3: Run the recovery test and verify GREEN**

Run: `pytest -q ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_source_chain_recovery.py`

Expected: PASS; `processor.py` imports and all recovered definitions are present.

### Task 3: Build the two deterministic runtime mirrors

**Files:**
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tools/build_chain_mirrors.py`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_mirror_completeness.py`
- Create under first destination: `runtime/app/**`, `annotations/**`, `manifests/**`, `tests/**`, `.env.example`, `.gitignore`
- Create under second destination: `runtime/app/**`, `annotations/**`, `manifests/**`, `tests/**`, `.env.example`, `.gitignore`

- [ ] **Step 1: Write failing mirror completeness tests**

```python
def test_target_definition_set_equals_source_definition_set(chain_manifest):
    assert chain_manifest["missing_definitions"] == []
    assert chain_manifest["extra_definitions"] == []

def test_every_source_physical_line_has_one_annotation(chain_manifest):
    assert chain_manifest["missing_annotation_lines"] == []
    assert chain_manifest["duplicate_annotation_lines"] == []
```

- [ ] **Step 2: Run tests and verify RED because mirrors do not exist**

Run: `pytest -q ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_mirror_completeness.py`

Expected: FAIL with missing manifest/runtime paths.

- [ ] **Step 3: Implement deterministic module copying**

The builder uses these seeds:

```python
FIRST_SEEDS = ["app.ai.processors.processor"]
SECOND_SEEDS = ["app.routers.vlm_router", "app.services.ai.extraction.process_service"]
```

It follows every project-local import in the full included modules, creates empty package `__init__.py` files where needed, copies source text without import rewrites, and prepends only a Chinese provenance comment containing source path and second-resolution migration time.

- [ ] **Step 4: Generate annotation ledgers and manifests**

For every source physical line, write one ledger row with `源行号`, `迁移时间`, `作用`, `理由/调用依据`, and JSON-escaped original text. Classify lines using Python tokenization and AST spans so imports, definitions, decorators, branches, returns, comments, strings and blanks receive specific Chinese explanations.

- [ ] **Step 5: Generate both mirrors and verify GREEN**

Run: `python ai-ie-backend/app/SQL_RAG/Knowledge_management/tools/build_chain_mirrors.py`

Expected: first manifest reports 17 project modules and 72 definitions; second reports 26 project modules and 117 definitions, adjusted only if the repaired source produces a documented, reviewable count change.

Run: `pytest -q ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_mirror_completeness.py`

Expected: PASS with zero missing definitions and zero missing/duplicate line annotations.

### Task 4: Configure target mirrors with the recorded credentials without exposing them

**Files:**
- Create ignored: `<first-destination>/runtime/.env`
- Create ignored: `<second-destination>/runtime/.env`
- Create tracked: `<first-destination>/.env.example`
- Create tracked: `<second-destination>/.env.example`
- Test: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_runtime_configuration.py`

- [ ] **Step 1: Write a failing configuration parity test**

```python
def test_required_secret_values_match_source_without_logging_values(source_env, target_env):
    required = {
        "EMBEDDING_SERVICE_API_KEY", "EMBEDDING_SERVICE_URL", "VLM_LLM_MODEL",
        "VISION_MODEL", "EMBEDDING_MODEL_VLM", "AUDIO_TRANSCRIPTION_MODEL",
        "DATABASE_URL", "DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD",
        "VECTOR_DB_TYPE", "VECTOR_DB_CONTEXT",
    }
    assert required <= source_env.keys()
    assert {key: bool(target_env.get(key)) for key in required} == {key: True for key in required}
    assert all(target_env[key] == source_env[key] for key in required)
```

- [ ] **Step 2: Verify RED before credential provisioning**

Run: `pytest -q ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_runtime_configuration.py`

Expected: FAIL because target runtime `.env` files are absent.

- [ ] **Step 3: Provision the recorded runtime configuration**

Copy the source `.env` byte-for-byte to both ignored target runtime `.env` files so the copied programs use the same recorded API key, database password/full URL, model names and vector settings. Never print values. Generate `.env.example` by preserving every key name and replacing every value with an empty string.

- [ ] **Step 4: Verify parity and Git exclusion**

Run: `pytest -q ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_runtime_configuration.py`

Expected: PASS.

Run: compare SHA256 for the source `.env` and both target runtime `.env` files.

Expected: all three hashes are identical; only hash strings are logged.

Run: `git check-ignore -v <first-runtime-env> <second-runtime-env>`

Expected: both files are ignored.

### Task 5: Test every file parsing branch and Qdrant boundary

**Files:**
- Create: `<first-destination>/tests/test_processor_flow.py`
- Create: `<first-destination>/tests/test_indexing_flow.py`
- Create: `<first-destination>/tests/test_runtime_trace.py`

- [ ] **Step 1: Write RED tests for text, document, image, OCR, audio, folder, export and unsupported branches**

Use real temporary files for validation and text reads. Patch only external model/Docling/FFmpeg boundaries, then assert dispatcher inputs, engine names, normalized result shapes, export paths and folder error isolation.

- [ ] **Step 2: Run and verify failures identify missing runtime wiring**

Run from the first runtime root with its `PYTHONPATH`: `pytest -q ../tests`

Expected: initial failures identify configuration/import differences rather than skipped branches.

- [ ] **Step 3: Fix only proven mirror/runtime defects**

Do not alter business mappings. Any fix must first have a failing test and a recorded root cause.

- [ ] **Step 4: Test Qdrant transformation and write boundary**

Assert `to_index_item`, `enrich_index_item`, document construction, empty-content rejection and an in-memory Qdrant write. Probe the configured real Qdrant endpoint separately and record its status without substituting a mock result for real connectivity.

- [ ] **Step 5: Verify all first-chain tests pass**

Run: `pytest -q <first-destination>/tests`

Expected: all branch tests pass; runtime trace contains every first-chain business definition intended to execute.

### Task 6: Test extraction orchestration and database mappings in isolation

**Files:**
- Create: `<second-destination>/tests/test_extraction_flow.py`
- Create: `<second-destination>/tests/test_database_mapping.py`
- Create: `<second-destination>/tests/test_upload_cleanup.py`

- [ ] **Step 1: Write RED orchestration tests**

Use deterministic fake LLM JSON and transaction-scoped/in-memory database boundaries to assert the order: upload → parse → raw save → QA → description → merge → intent → QA save → intent save → optional export → cleanup.

- [ ] **Step 2: Write RED field mapping tests**

Assert every screenshot field maps from the expected AI result key, including evidence extraction and status conversion.

- [ ] **Step 3: Run tests and fix only observed target defects**

Run: `pytest -q <second-destination>/tests -k "not live"`

Expected: PASS after runtime imports and local configuration are correct.

### Task 7: Execute real SiliconFlow DeepSeek and PostgreSQL integration test

**Files:**
- Create: `<second-destination>/tests/test_live_siliconflow_database_flow.py`
- Create: `<second-destination>/manifests/live_test_report.json`

- [ ] **Step 1: Check prerequisites without revealing secrets**

Validate only booleans/host reachability: API key non-empty, API base host reachable, configured model contains `DeepSeek`, database `SELECT 1` succeeds, and target mirror imports from its own runtime path.

- [ ] **Step 2: Call the target mirror's real SiliconFlow client**

Use a unique Chinese sample containing an explicit question, answer, evidence and intent. Call `extract_audio_knowledge` through the copied target module and assert QA/description/intent outputs parse into non-empty dictionaries.

- [ ] **Step 3: Run the copied upload-to-database pipeline**

Call `process_uploaded_file(action="analyze")` with a unique marker, capture `raw_data_id`, `qa_pair_ids` and `intent_ids`, then query the three database tables using the copied ORM models.

- [ ] **Step 4: Verify persisted fields and cleanup**

Assert all required screenshot fields and foreign-key IDs. Delete only records whose IDs were generated by this test, in child-to-parent order, and verify query counts return to zero.

- [ ] **Step 5: Write a redacted live report**

Record UTC/local timestamps, target module paths, model name, endpoint host, database host, generated IDs, row counts, field-presence booleans, cleanup counts and exceptions. Exclude credentials, full URLs containing passwords and full AI/customer text.

### Task 8: Final audit and completion verification

**Files:**
- Modify: both `manifests/execution_order.md`
- Modify: both `manifests/definitions.json`
- Modify: both `manifests/source_hashes.json`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/VERIFICATION_REPORT_2026-07-03.md`

- [ ] **Step 1: Run syntax and import verification**

Run: `python -m compileall -q <first-runtime> <second-runtime>`

Expected: exit code 0.

- [ ] **Step 2: Run the entire Knowledge_management test suite**

Run: `pytest -q ai-ie-backend/app/SQL_RAG/Knowledge_management/tests <first-tests> <second-tests>`

Expected: zero failed tests and no silently skipped required live test.

- [ ] **Step 3: Rebuild and compare deterministic artifacts**

Run the mirror builder again and verify `git diff --check`, definition counts, annotation coverage and hashes remain stable except for explicitly timestamped report fields.

- [ ] **Step 4: Audit Git scope**

Confirm changed paths are limited to the damaged source file and backup, the two requested target directories, Knowledge_management tools/tests/report, and Superpowers documentation.

- [ ] **Step 5: Write the verification report**

List every module and definition count, branch test evidence, real API/database evidence, Qdrant status, source recovery hashes, cleanup confirmation and any objective limitation. Do not claim completion unless every required check has fresh passing evidence.
