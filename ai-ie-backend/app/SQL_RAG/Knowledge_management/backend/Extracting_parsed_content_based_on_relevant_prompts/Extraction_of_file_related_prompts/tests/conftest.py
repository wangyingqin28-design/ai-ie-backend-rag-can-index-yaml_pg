"""第二条链测试的公共运行时与提取专属包加载夹具。"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest


CHAIN_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = CHAIN_ROOT / "runtime"
PUBLIC_RUNTIME_ROOT = CHAIN_ROOT.parents[1] / "public_program_files" / "runtime"


def _purge_app_modules() -> None:
    for name in list(sys.modules):
        if (
            name == "app"
            or name.startswith("app.")
            or name == "extraction_chain"
            or name.startswith("extraction_chain.")
        ):
            sys.modules.pop(name, None)


@pytest.fixture
def second_runtime(monkeypatch: pytest.MonkeyPatch):
    """确保公共 app 与 extraction_chain 均来自去重后的目标目录。"""

    _purge_app_modules()
    monkeypatch.syspath_prepend(str(RUNTIME_ROOT))
    monkeypatch.syspath_prepend(str(PUBLIC_RUNTIME_ROOT))
    monkeypatch.chdir(PUBLIC_RUNTIME_ROOT)
    importlib.invalidate_caches()
    yield RUNTIME_ROOT
    _purge_app_modules()
    importlib.invalidate_caches()
