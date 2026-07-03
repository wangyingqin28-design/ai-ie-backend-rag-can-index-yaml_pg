# Knowledge Chain Deduplication and Inline Comments Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace two duplicated runtime trees with one public runtime and two business-only packages, give every runtime code line an inline timestamped Chinese explanation, and prove the refactor with real audio transcription, DeepSeek extraction, database verification, and cleanup.

**Architecture:** `public_program_files/runtime/app` owns the former 27-file shared `app` tree and the only runtime `.env`. `parsing_logic/runtime/file_parsing_chain` is a thin public parsing facade; `Extraction_of_file_related_prompts/runtime/extraction_chain` owns only extraction, ORM, persistence, and routing code. A deterministic generator rewrites multiline string literals into equivalent adjacent fragments, inserts inline Chinese comments before every physical code line, and emits ownership and coverage manifests.

**Tech Stack:** Python 3.13, AST/tokenize, pytest, FastAPI, OpenAI-compatible SiliconFlow APIs, FFmpeg, SQLAlchemy/PostgreSQL, Docling, LlamaIndex, Qdrant, PowerShell, Git.

---

### Task 1: Establish failing ownership and inline-comment tests

**Files:**
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_refactored_layout.py`
- Create: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_inline_comment_coverage.py`
- Test: the two files above

- [ ] **Step 1: Write the failing duplicate-layout test**

```python
def test_business_directories_do_not_contain_public_app_tree():
    assert not (FIRST_ROOT / "runtime/app").exists()
    assert not (SECOND_ROOT / "runtime/app").exists()
    assert (PUBLIC_ROOT / "runtime/app").is_dir()


def test_no_identical_python_files_cross_ownership_boundaries():
    groups = [python_hashes(PUBLIC_ROOT), python_hashes(FIRST_ROOT), python_hashes(SECOND_ROOT)]
    for left_index, left in enumerate(groups):
        for right in groups[left_index + 1:]:
            assert set(left.values()).isdisjoint(right.values())
```

- [ ] **Step 2: Write the failing inline coverage test**

```python
ANNOTATION = re.compile(
    r"^\s*# \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] "
    r"作用：.+；理由依据：.+$"
)


def test_every_runtime_code_line_has_inline_chinese_annotation():
    for path in runtime_python_files():
        lines = path.read_text(encoding="utf-8").splitlines()
        assert all(line.strip() for line in lines)
        for index, line in enumerate(lines):
            if line.lstrip().startswith("#"):
                continue
            assert index > 0
            assert ANNOTATION.match(lines[index - 1])
```

- [ ] **Step 3: Verify RED**

Run:

`python -m pytest -q -p no:cacheprovider tests/test_refactored_layout.py tests/test_inline_comment_coverage.py`

Expected: failures show both old `runtime/app` trees exist, `public_program_files` is absent, and inline annotation coverage is below 100%.

### Task 2: Refactor the deterministic mirror generator

**Files:**
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tools/build_chain_mirrors.py`
- Test: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_chain_inventory.py`
- Test: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_refactored_layout.py`

- [ ] **Step 1: Add explicit ownership constants**

The generator must define:

```python
PUBLIC_ROOT = KNOWLEDGE_ROOT / "backend/public_program_files"
FIRST_ROOT = KNOWLEDGE_ROOT / "backend/File_parsing/parsing_logic"
SECOND_ROOT = (
    KNOWLEDGE_ROOT
    / "backend/Extracting_parsed_content_based_on_relevant_prompts"
    / "Extraction_of_file_related_prompts"
)
PUBLIC_MODULES = {
    "app.config",
    "app.ai.llm.llm_client",
    "app.ai.prompts",
    "app.ai.processors.audio_long_service",
    "app.ai.processors.audio_service",
    "app.ai.processors.document_service",
    "app.ai.processors.export_service",
    "app.ai.processors.file_utils",
    "app.ai.processors.image_service",
    "app.ai.processors.llamaindex_service",
    "app.ai.processors.processor",
    "app.ai.rag.vector_index_service",
    "app.query.query",
    "app.services.ai.indexing.knowledge_index_service",
    "app.vectorstore.base",
    "app.vectorstore.connector",
    "app.vectorstore.qdrant_connector",
}
```

Required package `__init__.py` files are generated in the public tree but are not duplicated elsewhere.

- [ ] **Step 2: Add the first-chain facade source**

Generate `runtime/file_parsing_chain/entry.py` with `parse_file`, `parse_folder`, `to_index_item`, `index_file`, and `index_folder`. Each function imports and delegates to the corresponding public `app.ai.processors.processor` or `app.services.ai.indexing.knowledge_index_service` function.

- [ ] **Step 3: Add extraction ownership mapping**

Copy these source modules into `runtime/extraction_chain`:

```text
process_service.py
audio_knowledge_extract_service.py
raw_data_service.py
qa_pair_service.py
intent_service.py
erp_ai_models.py
model_base.py
snowflake_generator.py
vlm_router.py
```

Apply deterministic import replacements:

```text
app.services.ai.extraction.audio_knowledge_extract_service -> extraction_chain.audio_knowledge_extract_service
app.services.ai.extraction.process_service -> extraction_chain.process_service
app.services.ai.knowledge.raw_data_service -> extraction_chain.raw_data_service
app.services.ai.knowledge.qa_pair_service -> extraction_chain.qa_pair_service
app.services.ai.knowledge.intent_service -> extraction_chain.intent_service
app.models.erp_ai_models -> extraction_chain.erp_ai_models
app.models.base -> extraction_chain.model_base
app.utils.snowflake_generator -> extraction_chain.snowflake_generator
```

Public imports such as `app.config`, `app.ai.processors.processor`, `app.ai.prompts`, and `app.ai.llm.llm_client` remain public.

- [ ] **Step 4: Add safe generated-path cleanup**

Resolve each cleanup target and assert it is a descendant of `Knowledge_management/backend` and one of:

```text
public_program_files
File_parsing/parsing_logic
Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts
```

Remove only old generated `runtime`, `annotations`, `manifests`, and chain-owned `tests` directories after new tests exist. Preserve `.env` bytes before cleanup and provision one ignored copy at `public_program_files/runtime/.env`.

- [ ] **Step 5: Run generator and layout tests**

Run:

`python tools/build_chain_mirrors.py`

Then:

`python -m pytest -q -p no:cacheprovider tests/test_refactored_layout.py`

Expected: public runtime exists; both business `runtime/app` directories and both old `annotations` directories are absent; cross-owner duplicate Python hashes equal zero.

### Task 3: Generate executable 100% inline comments

**Files:**
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tools/build_chain_mirrors.py`
- Test: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_inline_comment_coverage.py`
- Test: `ai-ie-backend/app/SQL_RAG/Knowledge_management/tests/test_mirror_completeness.py`

- [ ] **Step 1: Add multiline string normalization**

Use `tokenize.generate_tokens` to locate every `STRING` token whose start and end rows differ. Evaluate plain string tokens with `ast.literal_eval`, split the value with `splitlines(keepends=True)`, and replace the token with a parenthesized sequence of `repr(fragment)` expressions. Preserve indentation, assignment prefixes, expression suffixes, and exact evaluated value.

Reject bytes strings and f-strings with a descriptive exception unless their token occupies one line. The current selected runtime modules contain no multiline bytes or f-string tokens.

- [ ] **Step 2: Add per-line comment generation**

For every transformed source line:

- Replace a blank line with a timestamped `作用：分隔相邻逻辑块` comment.
- Prepend a timestamped explanation before an original comment.
- Prepend a timestamped explanation before every code line.
- Include owning module, nearest AST class/function scope, and ownership layer in `理由依据`.
- Do not place comments in another directory.

- [ ] **Step 3: Preserve string semantics**

Extend the test to parse canonical and generated modules and compare ordered values for all AST string constants. Explicitly assert equality for:

```python
QA_EXTRACTION_PROMPT
OUTPUT_FORMAT_PROMPT
DESCRIPTION_PROMPT
YT_PROMPT
AUDIO_QA_USER_PROMPT_TEMPLATE
```

- [ ] **Step 4: Verify annotation coverage**

Run:

`python -m pytest -q -p no:cacheprovider tests/test_inline_comment_coverage.py tests/test_mirror_completeness.py`

Expected: every runtime code line has a directly preceding timestamped Chinese comment, no runtime file contains blank physical lines or multiline string tokens, and prompt values match the source.

### Task 4: Rewire and retest the first parsing chain

**Files:**
- Create: `backend/File_parsing/parsing_logic/tests/conftest.py`
- Create: `backend/File_parsing/parsing_logic/tests/test_file_parsing_entry.py`
- Create: `backend/File_parsing/parsing_logic/tests/test_public_indexing.py`
- Create: `backend/File_parsing/parsing_logic/manifests/execution_order.md`

- [ ] **Step 1: Write facade RED tests**

Tests load both `public_program_files/runtime` and `parsing_logic/runtime` on `sys.path`, import `file_parsing_chain.entry`, and assert all five facade functions exist and delegate to public functions.

- [ ] **Step 2: Verify RED before generation**

Run:

`python -m pytest -q -p no:cacheprovider backend/File_parsing/parsing_logic/tests`

Expected: import failure for `file_parsing_chain`.

- [ ] **Step 3: Generate facade and run all parsing branches**

Use real temporary text files and controlled external boundaries to test text, image, OCR, document, audio, folder, export, unsupported, index-item, file-index, folder-index, and in-memory Qdrant paths.

- [ ] **Step 4: Verify GREEN**

Run:

`python -m pytest -q -p no:cacheprovider backend/public_program_files/tests backend/File_parsing/parsing_logic/tests`

Expected: all public and first-chain tests pass with no warnings.

### Task 5: Rewire and retest the extraction chain

**Files:**
- Create: `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/conftest.py`
- Create: `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_extraction_flow.py`
- Create: `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_database_mapping.py`
- Create: `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_upload_cleanup.py`

- [ ] **Step 1: Write extraction package RED test**

Load `public_program_files/runtime` and the second runtime, import `extraction_chain.process_service`, and assert its imported `process_file` resolves to the public processor module.

- [ ] **Step 2: Verify RED before generation**

Run:

`python -m pytest -q -p no:cacheprovider backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests -k "not live"`

Expected: import failure for `extraction_chain`.

- [ ] **Step 3: Run deterministic extraction and ORM tests**

Verify QA → description → merge → intent order, upload → parse → raw save → QA save → intent save order, all screenshot field mappings, and temporary upload cleanup on success and failure.

- [ ] **Step 4: Verify GREEN**

Run the same command as Step 2.

Expected: all non-live extraction tests pass.

### Task 6: Run real audio transcription through SiliconFlow

**Files:**
- Create: `backend/File_parsing/parsing_logic/tests/test_live_audio_transcription.py`
- Create: `backend/File_parsing/parsing_logic/manifests/live_audio_transcription_report.json`

- [ ] **Step 1: Verify the selected original recording**

Run PowerShell checks for:

`C:\Users\DELL\Documents\WeChat Files\wxid_ahul2j69cxzm22\FileStorage\File\2025-12\18859060061(18859060061)_20251217154314.mp3`

Expected: file exists, length is 40704 bytes, and first bytes are `FF FB`.

- [ ] **Step 2: Install and verify FFmpeg**

Run:

`winget install --id Gyan.FFmpeg.Shared -e --accept-source-agreements --accept-package-agreements --silent`

Then locate `ffmpeg.exe`, prepend its directory to the test process PATH, and run `ffmpeg -version`.

Expected: exit code 0 and a version line.

- [ ] **Step 3: Run the public audio parser**

The live test imports `file_parsing_chain.entry`, calls `parse_file(recording_path, mode="audio")`, and asserts:

```python
assert result["success"] is True
assert result["file_type"] == "audio"
assert result["engine"] == "audio_asr_long"
assert result["result"]["text"].strip()
assert result["result"]["model"] == "FunAudioLLM/SenseVoiceSmall"
```

If the long-audio aggregate does not currently expose the model field, write a failing assertion first and then add the minimal propagation from each transcription result.

- [ ] **Step 4: Write a redacted transcription report**

Record the source file SHA256, byte length, FFmpeg version, SiliconFlow host, transcription model, text length, chunk count, and a one-way text SHA256. Do not record full transcript.

### Task 7: Feed real transcript to DeepSeek and database

**Files:**
- Create: `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests/test_live_audio_deepseek_database_flow.py`
- Create: `backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/manifests/live_audio_database_report.json`

- [ ] **Step 1: Use the actual transcription result**

The test calls the first-chain live parser for the selected MP3, then passes the returned text to `extraction_chain.process_service` through an `UploadFile`-compatible workflow or its fixed extraction helper. It must not substitute a handwritten transcript.

- [ ] **Step 2: Call real DeepSeek**

Assert the common config resolves:

```python
assert settings.embedding_service_url == "https://api.siliconflow.cn/v1"
assert settings.embedding_service_api_key
assert "deepseek" in settings.LLM_MODEL.lower()
```

Call QA, description, and intent extraction and require non-empty parsed results.

- [ ] **Step 3: Persist and verify rows**

Write unique-marker rows to `AI_YuanShishuju`, `AI_Wendajilu`, and `AI_Yitu`. Query and assert all screenshot fields, intent fields, and `Yssj_id` links.

- [ ] **Step 4: Clean and verify zero residual rows**

Delete QA, intent, and raw rows in that order, commit, and query all three tables. Expected remaining rows for the generated IDs: 0.

- [ ] **Step 5: Write a redacted live report**

Record model names, API/database hosts, IDs, row counts, field-presence booleans, cleanup counts, and transcript hash/length. Exclude secrets and transcript content.

### Task 8: Final completeness and regression audit

**Files:**
- Modify: `ai-ie-backend/app/SQL_RAG/Knowledge_management/VERIFICATION_REPORT_2026-07-03.md`
- Create: `backend/public_program_files/manifests/ownership.json`
- Create: `backend/public_program_files/manifests/inline_comment_coverage.json`

- [ ] **Step 1: Rebuild twice and verify deterministic output**

Run `python tools/build_chain_mirrors.py` twice. Compare runtime and manifest hashes excluding live report timestamps. Expected differences: none.

- [ ] **Step 2: Run syntax and import checks**

Run `python -m compileall -q` on all three runtime directories. Expected: exit code 0.

- [ ] **Step 3: Run all Python tests including live tests**

Run:

`python -m pytest -q -p no:cacheprovider tests backend/public_program_files/tests backend/File_parsing/parsing_logic/tests backend/Extracting_parsed_content_based_on_relevant_prompts/Extraction_of_file_related_prompts/tests`

Expected: zero failures and no required live test skipped.

- [ ] **Step 4: Run existing Node.js tests**

Run:

`node --test webui/tests/*.test.mjs`

Expected: 13 passed, 0 failed.

- [ ] **Step 5: Audit ownership, duplication, comments, secrets, and cleanup**

Verify:

- Cross-owner identical Python hashes: 0.
- Business `runtime/app` directories: absent.
- Old `annotations` directories: absent.
- Runtime code lines with compliant inline comments: 100%.
- Prompt string values: unchanged.
- Tracked `runtime/.env` files: 0.
- Public runtime `.env`: exists and hash matches recorded source `.env`.
- Live database remaining test rows: 0.
- Changed paths remain inside the approved target directories, tools/tests/report, and Superpowers documentation.

- [ ] **Step 6: Commit**

Stage only task paths and run `git diff --cached --check` plus staged secret scanning. Commit with:

`git commit -m "refactor: deduplicate knowledge processing chains"`
