"""两个执行链镜像的定义与逐物理行注释完整性测试。"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
FIRST_ROOT = (
    KNOWLEDGE_ROOT
    / "backend/File_parsing/parsing_logic"
)
SECOND_ROOT = (
    KNOWLEDGE_ROOT
    / "backend/Extracting_parsed_content_based_on_relevant_prompts"
    / "Extraction_of_file_related_prompts"
)


@pytest.mark.parametrize("chain_root", [FIRST_ROOT, SECOND_ROOT])
def test_target_definition_set_equals_source_definition_set(chain_root: Path) -> None:
    manifest_path = chain_root / "manifests/definitions.json"
    assert manifest_path.is_file(), f"缺少定义清单: {manifest_path}"

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert manifest["missing_definitions"] == []
    assert manifest["extra_definitions"] == []
    assert manifest["source_definition_count"] == manifest["target_definition_count"]


@pytest.mark.parametrize("chain_root", [FIRST_ROOT, SECOND_ROOT])
def test_every_source_physical_line_has_exactly_one_annotation(chain_root: Path) -> None:
    manifest_path = chain_root / "manifests/definitions.json"
    assert manifest_path.is_file(), f"缺少定义清单: {manifest_path}"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    for module in manifest["modules"]:
        annotation_path = chain_root / module["annotation_path"]
        assert annotation_path.is_file(), f"缺少逐行注释台账: {annotation_path}"
        source_path = Path(module["source_path"])
        source_lines = source_path.read_text(encoding="utf-8-sig").splitlines()

        rows = [
            json.loads(line)
            for line in annotation_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        annotated_lines = [row["源行号"] for row in rows]
        expected_lines = list(range(1, module["source_line_count"] + 1))

        assert annotated_lines == expected_lines
        assert [row["原始代码"] for row in rows] == source_lines
        assert all(row["迁移时间"] == manifest["generated_at"] for row in rows)
        assert all(row["作用"] and row["理由依据"] for row in rows)


@pytest.mark.parametrize("chain_root", [FIRST_ROOT, SECOND_ROOT])
def test_every_runtime_module_is_a_complete_source_copy(chain_root: Path) -> None:
    manifest = json.loads(
        (chain_root / "manifests/definitions.json").read_text(encoding="utf-8")
    )

    for module in manifest["modules"]:
        source = Path(module["source_path"]).read_text(encoding="utf-8-sig")
        target = (chain_root / module["target_relative"]).read_text(encoding="utf-8")
        provenance, copied_source = target.split("\n", 1)

        assert provenance.startswith("# [")
        assert "中文迁移说明" in provenance
        assert copied_source == source


@pytest.mark.parametrize("chain_root", [FIRST_ROOT, SECOND_ROOT])
def test_mirror_hash_manifest_covers_every_module(chain_root: Path) -> None:
    definitions = json.loads(
        (chain_root / "manifests/definitions.json").read_text(encoding="utf-8")
    )
    hashes = json.loads(
        (chain_root / "manifests/source_hashes.json").read_text(encoding="utf-8")
    )

    assert set(hashes["modules"]) == {
        module["module"] for module in definitions["modules"]
    }
    assert all(item["source_sha256"] for item in hashes["modules"].values())
    assert all(item["target_sha256"] for item in hashes["modules"].values())
