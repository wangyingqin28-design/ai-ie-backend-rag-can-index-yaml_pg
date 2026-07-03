"""公共运行配置与源记录配置的一致性测试。"""

from __future__ import annotations

import hashlib
from pathlib import Path

KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ENV = Path(
    r"D:\wkt\getsoft---ai-erp-backend-feature-rag-new\getsoft---ai-erp-backend\.env"
)
PUBLIC_ROOT = KNOWLEDGE_ROOT / "backend/public_program_files"
REQUIRED_KEYS = {
    "EMBEDDING_SERVICE_API_KEY",
    "EMBEDDING_SERVICE_URL",
    "VLM_LLM_MODEL",
    "VISION_MODEL",
    "EMBEDDING_MODEL_VLM",
    "AUDIO_TRANSCRIPTION_MODEL",
    "DATABASE_URL",
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
    "DB_USER",
    "DB_PASSWORD",
    "VECTOR_DB_TYPE",
    "VECTOR_DB_CONTEXT",
}


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _parse_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def test_runtime_env_is_byte_identical_to_recorded_source() -> None:
    target_env = PUBLIC_ROOT / "runtime/.env"
    assert target_env.is_file(), f"缺少目标运行配置: {target_env}"
    assert _sha256(target_env) == _sha256(SOURCE_ENV)

    source_values = _parse_env(SOURCE_ENV)
    target_values = _parse_env(target_env)
    assert REQUIRED_KEYS <= source_values.keys()
    assert all(source_values[key] for key in REQUIRED_KEYS)
    assert all(target_values[key] == source_values[key] for key in REQUIRED_KEYS)


def test_env_example_contains_names_but_no_values() -> None:
    source_values = _parse_env(SOURCE_ENV)
    example_values = _parse_env(PUBLIC_ROOT / ".env.example")

    assert set(example_values) == set(source_values)
    assert all(value == "" for value in example_values.values())
