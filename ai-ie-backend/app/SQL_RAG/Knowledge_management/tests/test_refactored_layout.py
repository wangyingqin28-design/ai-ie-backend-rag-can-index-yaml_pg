"""验证公共程序层与两条业务链路的最终所有权边界。"""

from __future__ import annotations

import hashlib
from pathlib import Path


KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
BACKEND_ROOT = KNOWLEDGE_ROOT / "backend"
PUBLIC_ROOT = BACKEND_ROOT / "public_program_files"
PARSING_ROOT = BACKEND_ROOT / "File_parsing" / "parsing_logic"
EXTRACTION_ROOT = (
    BACKEND_ROOT
    / "Extracting_parsed_content_based_on_relevant_prompts"
    / "Extraction_of_file_related_prompts"
)


def _python_hashes(root: Path) -> dict[str, list[Path]]:
    """按文件内容散列收集 Python 文件，用于发现跨所有权目录的重复副本。"""

    hashes: dict[str, list[Path]] = {}
    for path in sorted(root.rglob("*.py")):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        hashes.setdefault(digest, []).append(path)
    return hashes


def test_shared_runtime_exists_only_in_public_program_files() -> None:
    """两条业务链不得再分别保存完整的 ``runtime/app`` 公共副本。"""

    assert (PUBLIC_ROOT / "runtime" / "app").is_dir()
    assert not (PARSING_ROOT / "runtime" / "app").exists()
    assert not (EXTRACTION_ROOT / "runtime" / "app").exists()


def test_business_roots_keep_only_their_chain_packages() -> None:
    """业务目录应只保留薄入口或提取专属实现。"""

    assert (PARSING_ROOT / "runtime" / "file_parsing_chain" / "entry.py").is_file()
    assert (
        EXTRACTION_ROOT / "runtime" / "extraction_chain" / "process_service.py"
    ).is_file()


def test_no_python_file_is_duplicated_across_ownership_roots() -> None:
    """同一份 Python 实现不能同时存在于公共层和任一业务层。"""

    roots = (PUBLIC_ROOT, PARSING_ROOT, EXTRACTION_ROOT)
    owners_by_hash: dict[str, set[Path]] = {}
    files_by_hash: dict[str, list[Path]] = {}

    for root in roots:
        for digest, paths in _python_hashes(root).items():
            owners_by_hash.setdefault(digest, set()).add(root)
            files_by_hash.setdefault(digest, []).extend(paths)

    duplicates = {
        digest: paths
        for digest, paths in files_by_hash.items()
        if len(owners_by_hash[digest]) > 1
    }
    assert duplicates == {}


def test_environment_file_has_one_owner() -> None:
    """真实密钥配置只能由公共运行时持有，避免两条链产生配置漂移。"""

    assert (PUBLIC_ROOT / "runtime" / ".env").is_file()
    assert not (PARSING_ROOT / "runtime" / ".env").exists()
    assert not (EXTRACTION_ROOT / "runtime" / ".env").exists()
