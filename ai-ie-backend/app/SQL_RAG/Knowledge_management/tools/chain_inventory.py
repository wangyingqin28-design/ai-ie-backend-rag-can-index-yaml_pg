"""静态清点 Python 模块闭包及其全部类、函数定义。"""

from __future__ import annotations

import ast
from collections import deque
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Definition:
    """一个项目内类或函数定义的位置记录。"""

    module: str
    qualname: str
    kind: str
    lineno: int
    end_lineno: int

    def to_dict(self) -> dict[str, str | int]:
        """转换为可直接序列化到 JSON 的字典。"""

        return asdict(self)


def module_path(source_root: Path, module: str) -> Path | None:
    """把模块名解析为项目根目录下的 Python 文件。"""

    relative = Path(*module.split("."))
    module_file = source_root / relative.with_suffix(".py")
    if module_file.is_file():
        return module_file

    package_file = source_root / relative / "__init__.py"
    if package_file.is_file():
        return package_file

    return None


def _resolve_from_module(current_module: str, node: ast.ImportFrom) -> str:
    """依据当前包和相对层级解析 ``from`` 导入的基准模块。"""

    if node.level == 0:
        return node.module or ""

    package_parts = current_module.split(".")[:-1]
    keep_count = len(package_parts) - (node.level - 1)
    if keep_count < 0:
        return ""

    base_parts = package_parts[:keep_count]
    if node.module:
        base_parts.extend(node.module.split("."))
    return ".".join(base_parts)


def _project_imports(
    source_root: Path,
    current_module: str,
    tree: ast.AST,
) -> set[str]:
    """提取 AST 中模块级与函数内部的所有项目内导入。"""

    imports: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("app.") and module_path(source_root, alias.name):
                    imports.add(alias.name)
            continue

        if not isinstance(node, ast.ImportFrom):
            continue

        base_module = _resolve_from_module(current_module, node)
        if base_module.startswith("app.") and module_path(source_root, base_module):
            imports.add(base_module)

        for alias in node.names:
            candidate = f"{base_module}.{alias.name}" if base_module else alias.name
            if candidate.startswith("app.") and module_path(source_root, candidate):
                imports.add(candidate)

    return imports


def collect_module_closure(
    source_root: Path,
    seeds: Iterable[str],
) -> dict[str, Path]:
    """从入口模块递归收集完整的项目内导入闭包。"""

    root = source_root.resolve()
    queue = deque(seeds)
    modules: dict[str, Path] = {}

    while queue:
        module = queue.popleft()
        if module in modules:
            continue

        path = module_path(root, module)
        if path is None:
            raise ModuleNotFoundError(f"项目内模块不存在: {module}")

        source = path.read_text(encoding="utf-8-sig")
        tree = ast.parse(source, filename=str(path))
        modules[module] = path

        for dependency in sorted(_project_imports(root, module, tree)):
            if dependency not in modules:
                queue.append(dependency)

    return dict(sorted(modules.items()))


class _DefinitionVisitor(ast.NodeVisitor):
    """保留嵌套层级的定义访问器。"""

    def __init__(self, module: str) -> None:
        self.module = module
        self.scope: list[str] = []
        self.definitions: list[Definition] = []

    def _record(self, node: ast.AST, name: str, kind: str) -> None:
        qualname = ".".join([*self.scope, name])
        self.definitions.append(
            Definition(
                module=self.module,
                qualname=qualname,
                kind=kind,
                lineno=node.lineno,
                end_lineno=node.end_lineno or node.lineno,
            )
        )

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self._record(node, node.name, "class")
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self._record(node, node.name, "def")
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self._record(node, node.name, "async def")
        self.scope.append(node.name)
        self.generic_visit(node)
        self.scope.pop()


def collect_definitions(modules: dict[str, Path]) -> list[Definition]:
    """收集指定模块中的全部类、同步函数和异步函数。"""

    definitions: list[Definition] = []
    for module, path in sorted(modules.items()):
        source = path.read_text(encoding="utf-8-sig")
        tree = ast.parse(source, filename=str(path))
        visitor = _DefinitionVisitor(module)
        visitor.visit(tree)
        definitions.extend(visitor.definitions)

    return sorted(
        definitions,
        key=lambda item: (item.module, item.lineno, item.qualname),
    )
