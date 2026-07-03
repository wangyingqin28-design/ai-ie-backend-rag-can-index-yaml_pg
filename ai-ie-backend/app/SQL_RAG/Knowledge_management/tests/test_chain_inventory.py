"""项目内传递依赖与定义清点工具测试。"""

from __future__ import annotations

import sys
from pathlib import Path


KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
if str(KNOWLEDGE_ROOT) not in sys.path:
    sys.path.insert(0, str(KNOWLEDGE_ROOT))

from tools.chain_inventory import collect_definitions, collect_module_closure


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def test_collect_module_closure_follows_relative_and_nested_imports(tmp_path: Path) -> None:
    _write(tmp_path / "app/__init__.py", "")
    _write(tmp_path / "app/pkg/__init__.py", "")
    _write(
        tmp_path / "app/pkg/entry.py",
        "from .helper import run\n\ndef delayed():\n    from app.pkg.deep import finish\n    return finish()\n",
    )
    _write(tmp_path / "app/pkg/helper.py", "def run():\n    return 'run'\n")
    _write(tmp_path / "app/pkg/deep.py", "def finish():\n    return 'done'\n")

    modules = collect_module_closure(tmp_path, ["app.pkg.entry"])

    assert set(modules) == {
        "app.pkg.entry",
        "app.pkg.helper",
        "app.pkg.deep",
    }


def test_collect_definitions_qualifies_class_methods(tmp_path: Path) -> None:
    _write(tmp_path / "app/__init__.py", "")
    _write(
        tmp_path / "app/sample.py",
        "class Worker:\n    def run(self):\n        return 1\n\nasync def dispatch():\n    return 2\n",
    )

    definitions = collect_definitions({"app.sample": tmp_path / "app/sample.py"})

    assert {(item.qualname, item.kind) for item in definitions} == {
        ("Worker", "class"),
        ("Worker.run", "def"),
        ("dispatch", "async def"),
    }
