"""第一条链测试的公共运行时与薄业务入口加载夹具。"""

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
            or name == "file_parsing_chain"
            or name.startswith("file_parsing_chain.")
        ):
            sys.modules.pop(name, None)


@pytest.fixture
def first_runtime(monkeypatch: pytest.MonkeyPatch):
    """确保公共 app 和解析链薄入口按最终目录边界加载。"""

    _purge_app_modules()
    monkeypatch.syspath_prepend(str(RUNTIME_ROOT))
    monkeypatch.syspath_prepend(str(PUBLIC_RUNTIME_ROOT))
    monkeypatch.chdir(PUBLIC_RUNTIME_ROOT)
    importlib.invalidate_caches()
    yield RUNTIME_ROOT
    _purge_app_modules()
    importlib.invalidate_caches()
