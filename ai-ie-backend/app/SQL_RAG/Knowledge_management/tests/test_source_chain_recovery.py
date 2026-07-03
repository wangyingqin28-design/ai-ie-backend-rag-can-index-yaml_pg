"""源文件损坏恢复的回归测试。"""

from __future__ import annotations

import ast
from pathlib import Path


SOURCE_ROOT = Path(
    r"D:\wkt\getsoft---ai-erp-backend-feature-rag-new\getsoft---ai-erp-backend"
)
DOCUMENT_SERVICE = SOURCE_ROOT / "app/ai/processors/document_service.py"
PROCESSOR = SOURCE_ROOT / "app/ai/processors/processor.py"

EXPECTED_DOCUMENT_DEFINITIONS = {
    "_safe_export_to_markdown",
    "_safe_export_to_dict",
    "build_docling_converter",
    "parse_document_with_docling",
    "process_document_file",
    "query_document_with_llamaindex",
    "process_text_file",
}


def _top_level_definition_names(path: Path) -> set[str]:
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(path))
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    }


def test_source_chain_entry_modules_are_utf8_and_parseable() -> None:
    failures: list[tuple[str, str]] = []

    for path in (DOCUMENT_SERVICE, PROCESSOR):
        try:
            source = path.read_text(encoding="utf-8-sig")
            ast.parse(source, filename=str(path))
        except (UnicodeDecodeError, SyntaxError) as exc:
            failures.append((str(path), str(exc)))

    assert failures == []


def test_document_service_recovery_restores_every_expected_definition() -> None:
    assert _top_level_definition_names(DOCUMENT_SERVICE) == EXPECTED_DOCUMENT_DEFINITIONS
