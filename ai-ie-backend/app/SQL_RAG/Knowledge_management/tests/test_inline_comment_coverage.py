"""验证运行时代码逐行中文内联注释的强制覆盖规则。"""

from __future__ import annotations

import ast
import io
import re
import tokenize
from pathlib import Path


KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = KNOWLEDGE_ROOT / "backend"
RUNTIME_ROOTS = (
    BACKEND_ROOT / "public_program_files" / "runtime",
    BACKEND_ROOT / "File_parsing" / "parsing_logic" / "runtime",
    BACKEND_ROOT
    / "Extracting_parsed_content_based_on_relevant_prompts"
    / "Extraction_of_file_related_prompts"
    / "runtime",
)
ANNOTATION = re.compile(
    r"^\s*# \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] "
    r"作用：.+；理由依据：.+$"
)


def _runtime_python_files() -> list[Path]:
    return [
        path
        for root in RUNTIME_ROOTS
        if root.exists()
        for path in sorted(root.rglob("*.py"))
    ]


def test_every_runtime_physical_line_has_inline_chinese_explanation() -> None:
    """每一条代码或原注释前必须紧邻时间、作用和依据说明。"""

    files = _runtime_python_files()
    assert files
    missing: list[str] = []

    for path in files:
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            if not line.strip() or ANNOTATION.match(line):
                continue
            if index == 0 or not ANNOTATION.match(lines[index - 1]):
                missing.append(f"{path}:{index + 1}: {line}")

    assert missing == []


def test_runtime_files_have_no_unannotatable_blank_or_multiline_string() -> None:
    """空白行和跨物理行字符串必须被改写，否则无法满足逐行内联说明。"""

    failures: list[str] = []
    for path in _runtime_python_files():
        source = path.read_text(encoding="utf-8")
        if any(not line.strip() for line in source.splitlines()):
            failures.append(f"{path}: 存在空白物理行")

        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for token in tokens:
            if token.type == tokenize.STRING and token.start[0] != token.end[0]:
                failures.append(
                    f"{path}:{token.start[0]}: 存在跨物理行字符串"
                )

        ast.parse(source, filename=str(path))

    assert failures == []


def test_legacy_sidecar_annotation_directories_are_removed() -> None:
    """逐行说明必须直接写入程序文件，不能继续放在外部 JSONL 台账。"""

    annotation_dirs = [
        path
        for root in (
            BACKEND_ROOT / "File_parsing" / "parsing_logic",
            BACKEND_ROOT
            / "Extracting_parsed_content_based_on_relevant_prompts"
            / "Extraction_of_file_related_prompts",
        )
        for path in root.rglob("annotations")
    ]
    assert annotation_dirs == []


def test_comment_rewrite_preserves_all_canonical_string_values() -> None:
    """提示词和文档字符串可改写物理形式，但运行时字符串值不得变化。"""

    source_root = Path(
        r"D:\wkt\getsoft---ai-erp-backend-feature-rag-new"
        r"\getsoft---ai-erp-backend"
    )
    ownership = __import__("json").loads(
        (
            BACKEND_ROOT
            / "public_program_files/manifests/ownership.json"
        ).read_text(encoding="utf-8")
    )
    pairs: list[tuple[Path, Path]] = []
    for module in ownership["public_modules"]:
        relative = Path(*module.split(".")).with_suffix(".py")
        pairs.append(
            (
                source_root / relative,
                BACKEND_ROOT / "public_program_files/runtime" / relative,
            )
        )
    extraction_root = (
        BACKEND_ROOT
        / "Extracting_parsed_content_based_on_relevant_prompts"
        / "Extraction_of_file_related_prompts/runtime/extraction_chain"
    )
    for module, filename in ownership["extraction_module_targets"].items():
        pairs.append(
            (
                source_root / Path(*module.split(".")).with_suffix(".py"),
                extraction_root / filename,
            )
        )

    for source_path, target_path in pairs:
        source_tree = ast.parse(
            source_path.read_text(encoding="utf-8-sig"),
            filename=str(source_path),
        )
        target_tree = ast.parse(
            target_path.read_text(encoding="utf-8"),
            filename=str(target_path),
        )
        source_strings = [
            node.value
            for node in ast.walk(source_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        ]
        target_strings = [
            node.value
            for node in ast.walk(target_tree)
            if isinstance(node, ast.Constant) and isinstance(node.value, str)
        ]
        assert target_strings == source_strings
