"""公共层和业务层模块、定义与源散列的完整性审计。"""

from __future__ import annotations

import ast
import hashlib
import json
from pathlib import Path


KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = Path(
    r"D:\wkt\getsoft---ai-erp-backend-feature-rag-new\getsoft---ai-erp-backend"
)
PUBLIC_ROOT = KNOWLEDGE_ROOT / "backend/public_program_files"
PARSING_ROOT = KNOWLEDGE_ROOT / "backend/File_parsing/parsing_logic"
EXTRACTION_ROOT = (
    KNOWLEDGE_ROOT
    / "backend/Extracting_parsed_content_based_on_relevant_prompts"
    / "Extraction_of_file_related_prompts"
)


def _definitions(path: Path) -> set[tuple[str, str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    return {
        (node.name, type(node).__name__)
        for node in ast.walk(tree)
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
    }


def test_ownership_manifest_covers_all_source_definitions_and_hashes() -> None:
    manifest = json.loads(
        (PUBLIC_ROOT / "manifests/ownership.json").read_text(encoding="utf-8")
    )
    assert manifest["source_definition_count"] == 118
    assert len(manifest["source_definitions"]) == 118

    for module, expected_hash in manifest["source_hashes"].items():
        relative = Path(*module.split("."))
        source = SOURCE_ROOT / relative.with_suffix(".py")
        assert source.is_file()
        actual = hashlib.sha256(source.read_bytes()).hexdigest().upper()
        assert actual == expected_hash


def test_public_target_definitions_equal_their_canonical_sources() -> None:
    manifest = json.loads(
        (PUBLIC_ROOT / "manifests/ownership.json").read_text(encoding="utf-8")
    )
    for module in manifest["public_modules"]:
        relative = Path(*module.split(".")).with_suffix(".py")
        source = SOURCE_ROOT / relative
        target = PUBLIC_ROOT / "runtime" / relative
        assert _definitions(target) == {
            (node.name, type(node).__name__)
            for node in ast.walk(
                ast.parse(source.read_text(encoding="utf-8-sig"))
            )
            if isinstance(
                node,
                (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
            )
        }


def test_extraction_target_definitions_equal_their_canonical_sources() -> None:
    manifest = json.loads(
        (PUBLIC_ROOT / "manifests/ownership.json").read_text(encoding="utf-8")
    )
    target_root = EXTRACTION_ROOT / "runtime" / "extraction_chain"

    for module, filename in manifest["extraction_module_targets"].items():
        source = SOURCE_ROOT / Path(*module.split(".")).with_suffix(".py")
        target = target_root / filename
        source_definitions = {
            (node.name, type(node).__name__)
            for node in ast.walk(
                ast.parse(source.read_text(encoding="utf-8-sig"))
            )
            if isinstance(
                node,
                (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef),
            )
        }
        assert _definitions(target) == source_definitions


def test_chain_manifests_report_no_missing_or_extra_definitions() -> None:
    for root in (PARSING_ROOT, EXTRACTION_ROOT):
        manifest = json.loads(
            (root / "manifests/definitions.json").read_text(encoding="utf-8")
        )
        assert manifest["missing_definitions"] == []
        assert manifest["extra_definitions"] == []
