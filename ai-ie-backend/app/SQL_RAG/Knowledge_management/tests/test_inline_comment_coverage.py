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
    r"^\s*# \[(?P<timestamp>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\] "
    r"作用：(?P<purpose>.+)；理由依据：(?P<basis>.+)$"
)
DEFINITION = re.compile(
    r"^\s*(?:async\s+def|def|class)\s+(?P<name>[A-Za-z_]\w*)"
)
ASSIGNMENT = re.compile(
    r"^\s*(?P<name>[A-Za-z_]\w*)\s*(?::[^=]+)?=(?!=)"
)


def _runtime_python_files() -> list[Path]:
    return [
        path
        for root in RUNTIME_ROOTS
        if root.exists()
        for path in sorted(root.rglob("*.py"))
    ]


def test_every_code_line_has_exactly_one_immediately_adjacent_explanation() -> None:
    """每条代码前只能有一条说明，说明后不能再出现空白或其他注释。"""

    files = _runtime_python_files()
    assert files
    failures: list[str] = []

    for path in files:
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, line in enumerate(lines):
            annotation = ANNOTATION.match(line)
            if annotation:
                if index + 1 >= len(lines):
                    failures.append(f"{path}:{index + 1}: 文件末尾孤立说明")
                    continue
                following = lines[index + 1]
                if not following.strip() or following.lstrip().startswith("#"):
                    failures.append(
                        f"{path}:{index + 1}: 说明后没有立即对应代码"
                    )
                continue
            if not line.strip():
                failures.append(f"{path}:{index + 1}: 存在空白行")
                continue
            if line.lstrip().startswith("#"):
                failures.append(f"{path}:{index + 1}: 存在独立原注释")
                continue
            if index == 0 or not ANNOTATION.match(lines[index - 1]):
                failures.append(f"{path}:{index + 1}: 代码前缺少唯一说明")

    assert failures == []


def test_explanation_names_the_definition_or_assignment_it_describes() -> None:
    """关键声明的说明必须点名对应类、函数、变量或 ORM 字段。"""

    failures: list[str] = []
    for path in _runtime_python_files():
        lines = path.read_text(encoding="utf-8").splitlines()
        for index, code in enumerate(lines):
            if index == 0 or code.lstrip().startswith("#"):
                continue
            annotation = ANNOTATION.match(lines[index - 1])
            if not annotation:
                continue
            declared = DEFINITION.match(code) or ASSIGNMENT.match(code)
            if declared and declared.group("name") not in annotation.group("purpose"):
                failures.append(
                    f"{path}:{index + 1}: 说明未点名 {declared.group('name')}"
                )

    assert failures == []


def test_generated_explanations_do_not_copy_garbled_source_comments() -> None:
    """生成说明只描述实际代码，不复制可能受加密或编码影响的原注释乱码。"""

    failures: list[str] = []
    for path in _runtime_python_files():
        for index, line in enumerate(
            path.read_text(encoding="utf-8").splitlines(),
            start=1,
        ):
            if ANNOTATION.match(line) and (
                "???" in line or "\ufffd" in line or "\x00" in line
            ):
                failures.append(f"{path}:{index}: 说明包含乱码")

    assert failures == []


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
