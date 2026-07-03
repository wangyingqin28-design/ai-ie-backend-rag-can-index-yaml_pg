"""第二条链测试的私有运行镜像加载夹具。"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest


CHAIN_ROOT = Path(__file__).resolve().parents[1]
RUNTIME_ROOT = CHAIN_ROOT / "runtime"


def _purge_app_modules() -> None:
    for name in list(sys.modules):
        if name == "app" or name.startswith("app."):
            sys.modules.pop(name, None)


@pytest.fixture
def second_runtime(monkeypatch: pytest.MonkeyPatch):
    """确保 app.* 来自第二条链自己的 runtime。"""

    _purge_app_modules()
    monkeypatch.syspath_prepend(str(RUNTIME_ROOT))
    monkeypatch.chdir(RUNTIME_ROOT)
    importlib.invalidate_caches()
    yield RUNTIME_ROOT
    _purge_app_modules()
    importlib.invalidate_caches()
