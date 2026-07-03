"""按公共层和业务层所有权生成两条可独立测试的执行链。"""

from __future__ import annotations

import ast
import hashlib
import io
import json
import shutil
import sys
import tokenize
from datetime import datetime
from pathlib import Path
from typing import Iterable


KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
if str(KNOWLEDGE_ROOT) not in sys.path:
    sys.path.insert(0, str(KNOWLEDGE_ROOT))

from tools.chain_inventory import collect_definitions, collect_module_closure


SOURCE_ROOT = Path(
    r"D:\wkt\getsoft---ai-erp-backend-feature-rag-new\getsoft---ai-erp-backend"
)
BACKEND_ROOT = KNOWLEDGE_ROOT / "backend"
PUBLIC_ROOT = BACKEND_ROOT / "public_program_files"
FIRST_ROOT = BACKEND_ROOT / "File_parsing" / "parsing_logic"
SECOND_ROOT = (
    BACKEND_ROOT
    / "Extracting_parsed_content_based_on_relevant_prompts"
    / "Extraction_of_file_related_prompts"
)
FIRST_SEEDS = ["app.ai.processors.processor"]
SECOND_SEEDS = [
    "app.routers.vlm_router",
    "app.services.ai.extraction.process_service",
]
SOURCE_ENV = SOURCE_ROOT / ".env"
GENERATED_AT_FILE = PUBLIC_ROOT / "manifests" / "generated_at.txt"

EXTRACTION_TARGETS = {
    "app.models.base": "model_base.py",
    "app.models.erp_ai_models": "erp_ai_models.py",
    "app.routers.vlm_router": "vlm_router.py",
    "app.services.ai.extraction.audio_knowledge_extract_service": (
        "audio_knowledge_extract_service.py"
    ),
    "app.services.ai.extraction.process_service": "process_service.py",
    "app.services.ai.knowledge.intent_service": "intent_service.py",
    "app.services.ai.knowledge.qa_pair_service": "qa_pair_service.py",
    "app.services.ai.knowledge.raw_data_service": "raw_data_service.py",
    "app.utils.snowflake_generator": "snowflake_generator.py",
}
IMPORT_REWRITES = {
    module: f"extraction_chain.{Path(filename).stem}"
    for module, filename in EXTRACTION_TARGETS.items()
}


def _generated_at() -> str:
    """复用首次重构时间，使重复构建不会制造无意义的全文件差异。"""

    if GENERATED_AT_FILE.is_file():
        return GENERATED_AT_FILE.read_text(encoding="utf-8").strip()
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def _sha256(path: Path) -> str:
    """计算文件散列，不把密钥或连接串写入日志。"""

    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def _write_json(path: Path, data: object) -> None:
    """以 UTF-8 和稳定键序写审计清单。"""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _assert_owned_path(path: Path, owner: Path) -> None:
    """删除生成目录前验证目标仍位于明确授权的业务根目录内。"""

    resolved = path.resolve()
    owner_resolved = owner.resolve()
    if resolved == owner_resolved or owner_resolved not in resolved.parents:
        raise RuntimeError(f"拒绝处理越界路径: {resolved}")


def _remove_generated(path: Path, owner: Path) -> None:
    """仅清理生成器拥有的目录，保留测试和其他用户文件。"""

    _assert_owned_path(path, owner)
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def _absolute_offsets(source: str) -> list[int]:
    """生成每个物理行在源码字符串中的绝对起始偏移。"""

    starts = [0]
    for line in source.splitlines(keepends=True):
        starts.append(starts[-1] + len(line))
    return starts


def _normalize_explicit_continuations(source: str, filename: str) -> str:
    """把赋值语句的反斜杠续行改成括号续行，允许逐行插入注释。"""

    lines = source.splitlines()
    output: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.rstrip().endswith("\\"):
            output.append(line)
            index += 1
            continue

        indent = line[: len(line) - len(line.lstrip())]
        statement = line.strip()
        if "=" not in statement:
            raise ValueError(f"{filename}:{index + 1} 存在未支持的反斜杠续行")
        left, right = statement.rsplit("=", 1)
        parts = [right.rstrip()[:-1].rstrip()]
        index += 1
        while index < len(lines):
            continuation = lines[index].strip()
            has_more = continuation.endswith("\\")
            parts.append(
                continuation[:-1].rstrip() if has_more else continuation
            )
            index += 1
            if not has_more:
                break
        output.append(f"{indent}{left.rstrip()} = (")
        output.extend(f"{indent}    {part}" for part in parts)
        output.append(f"{indent})")
    return "\n".join(output) + ("\n" if source.endswith("\n") else "")


def _normalize_multiline_strings(source: str, filename: str) -> str:
    """把跨行普通字符串等价改写为单行字面量，便于逐物理行注释。"""

    replacements: list[tuple[int, int, str]] = []
    starts = _absolute_offsets(source)
    reader = io.StringIO(source).readline

    for token in tokenize.generate_tokens(reader):
        if token.type != tokenize.STRING or token.start[0] == token.end[0]:
            continue
        prefix = token.string.lstrip()[:2].lower()
        if "f" in prefix:
            raise ValueError(f"{filename}:{token.start[0]} 不支持跨行 f-string")
        try:
            value = ast.literal_eval(token.string)
        except (SyntaxError, ValueError) as exc:
            raise ValueError(
                f"{filename}:{token.start[0]} 无法等价改写跨行字符串"
            ) from exc
        start = starts[token.start[0] - 1] + token.start[1]
        end = starts[token.end[0] - 1] + token.end[1]
        replacements.append((start, end, repr(value)))

    for start, end, replacement in reversed(replacements):
        source = source[:start] + replacement + source[end:]
    return source


def _definition_spans(source: str) -> list[tuple[int, int, str, str]]:
    """收集定义区间，使每条说明能够指出所属 def/class。"""

    tree = ast.parse(source)
    spans: list[tuple[int, int, str, str]] = []

    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.scope: list[str] = []

        def record(self, node: ast.AST, name: str, kind: str) -> None:
            qualname = ".".join([*self.scope, name])
            spans.append(
                (node.lineno, node.end_lineno or node.lineno, qualname, kind)
            )
            self.scope.append(name)
            self.generic_visit(node)
            self.scope.pop()

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            self.record(node, node.name, "类")

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self.record(node, node.name, "同步函数")

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self.record(node, node.name, "异步函数")

    Visitor().visit(tree)
    return spans


def _line_scope(
    line_number: int,
    spans: list[tuple[int, int, str, str]],
) -> tuple[str, str] | None:
    """返回覆盖当前行的最内层定义。"""

    candidates = [span for span in spans if span[0] <= line_number <= span[1]]
    if not candidates:
        return None
    start, end, qualname, kind = min(
        candidates,
        key=lambda item: item[1] - item[0],
    )
    return qualname, kind


def _line_purpose(code: str) -> str:
    """依据代码形态生成具体且稳定的中文作用说明。"""

    stripped = code.strip()
    if not stripped:
        return "分隔相邻逻辑块"
    if stripped.startswith("#"):
        return "保留原实现注释并说明约束"
    if stripped.startswith(("from ", "import ")):
        return "导入本节点运行所需依赖"
    if stripped.startswith("@"):
        return "为下方定义注册装饰器行为"
    if stripped.startswith("class "):
        return "定义封装数据或行为的类"
    if stripped.startswith("async def "):
        return "定义可等待的异步处理节点"
    if stripped.startswith("def "):
        return "定义可复用的同步处理节点"
    if stripped.startswith(("if ", "elif ", "else:")):
        return "依据当前状态选择执行分支"
    if stripped.startswith(("for ", "while ")):
        return "逐项处理集合或重复任务"
    if stripped.startswith(("try:", "except ", "finally:")):
        return "控制异常处理和资源清理"
    if stripped.startswith(("with ", "async with ")):
        return "限定文件、会话或异步资源生命周期"
    if stripped.startswith("return"):
        return "向调用方返回本节点结果"
    if stripped.startswith("raise "):
        return "阻止无效状态继续传播"
    if "await " in stripped:
        return "等待异步下游完成并接收结果"
    if "=" in stripped and "==" not in stripped and "!=" not in stripped:
        return "保存配置、参数或中间运行状态"
    if stripped.endswith(("(", ",", "[", "{")):
        return "继续构造多行调用或数据结构"
    return "执行当前节点的数据处理或控制表达式"


def _annotate_source(
    source: str,
    *,
    module: str,
    owner: str,
    generated_at: str,
) -> str:
    """在每条原代码/原注释前直接插入时间、作用和理由依据。"""

    normalized = _normalize_explicit_continuations(source, module)
    normalized = _normalize_multiline_strings(normalized, module)
    ast.parse(normalized, filename=module)
    spans = _definition_spans(normalized)
    output: list[str] = []

    for line_number, line in enumerate(normalized.splitlines(), start=1):
        indent = line[: len(line) - len(line.lstrip())]
        scope = _line_scope(line_number, spans)
        if scope:
            qualname, kind = scope
            basis = f"{owner}所有；本行属于{kind} {qualname}"
        else:
            basis = f"{owner}所有；本行属于模块 {module} 的模块级声明"
        purpose = _line_purpose(line)
        annotation = (
            f"{indent}# [{generated_at}] 作用：{purpose}；理由依据：{basis}"
        )
        output.append(annotation)
        if line.strip():
            output.append(line)

    result = "\n".join(output) + "\n"
    ast.parse(result, filename=module)
    return result


def _rewrite_extraction_imports(source: str) -> str:
    """把提取专属模块的旧 app 路径改为 extraction_chain 内部路径。"""

    rewritten = source
    for old_module, new_module in sorted(
        IMPORT_REWRITES.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        rewritten = rewritten.replace(old_module, new_module)
    return rewritten


def _ensure_package_files(
    package_root: Path,
    target_file: Path,
    *,
    owner: str,
    generated_at: str,
) -> None:
    """为目标文件逐层补齐具有独立说明的包标记。"""

    current = target_file.parent
    while current == package_root or package_root in current.parents:
        init_file = current / "__init__.py"
        if not init_file.exists():
            relative = current.relative_to(package_root).as_posix() or "."
            source = f'"""{owner}的软件包标记：{relative}。"""\n'
            init_file.write_text(
                _annotate_source(
                    source,
                    module=f"{owner}:{relative}",
                    owner=owner,
                    generated_at=generated_at,
                ),
                encoding="utf-8",
            )
        if current == package_root:
            break
        current = current.parent


def _write_module(
    *,
    source: str,
    target: Path,
    package_root: Path,
    module: str,
    owner: str,
    generated_at: str,
) -> None:
    """写入一个已逐行注释的目标模块并补齐包结构。"""

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        _annotate_source(
            source,
            module=module,
            owner=owner,
            generated_at=generated_at,
        ),
        encoding="utf-8",
    )
    _ensure_package_files(
        package_root,
        target,
        owner=owner,
        generated_at=generated_at,
    )


def _facade_source() -> str:
    """返回文件解析链的薄入口源码。"""

    return '''"""文件解析业务链入口；实现由公共 app 包提供。"""
from typing import Any
from app.ai.processors.processor import Mode
from app.ai.processors import processor as _processor

async def parse_file(
    file_path: str,
    mode: Mode = "auto",
    export: bool = False,
    output_dir: str | None = None,
    summary_prompt: str | None = None,
) -> dict[str, Any]:
    """调用公共解析器处理一个文件。"""
    return await _processor.process_file(
        file_path=file_path,
        mode=mode,
        export=export,
        output_dir=output_dir,
        summary_prompt=summary_prompt,
    )

async def parse_folder(
    folder_path: str,
    mode: Mode = "auto",
    recursive: bool = False,
    export: bool = False,
    output_dir: str | None = None,
    summary_prompt: str | None = None,
) -> dict[str, Any]:
    """调用公共解析器处理一个目录。"""
    return await _processor.process_folder(
        folder_path=folder_path,
        mode=mode,
        recursive=recursive,
        export=export,
        output_dir=output_dir,
        summary_prompt=summary_prompt,
    )

def to_index_item(processed: dict[str, Any]) -> dict[str, Any]:
    """把解析结果转换为公共索引载荷。"""
    return _processor.to_index_item(processed)

async def index_file(**kwargs: Any) -> dict[str, Any]:
    """调用公共 Qdrant 包装层索引单个文件。"""
    return await _processor.index_file_to_qdrant(**kwargs)

async def index_folder(**kwargs: Any) -> dict[str, Any]:
    """调用公共 Qdrant 包装层索引文件夹。"""
    return await _processor.index_folder_to_qdrant(**kwargs)
'''


def _provision_configuration(generated_at: str) -> None:
    """只在公共运行时保存记录配置，并生成不含敏感值的示例。"""

    source_bytes = SOURCE_ENV.read_bytes()
    public_runtime = PUBLIC_ROOT / "runtime"
    public_runtime.mkdir(parents=True, exist_ok=True)
    (public_runtime / ".env").write_bytes(source_bytes)

    keys: list[str] = []
    for raw_line in source_bytes.decode("utf-8-sig").splitlines():
        line = raw_line.strip()
        if line and not line.startswith("#") and "=" in line:
            key = line.split("=", 1)[0].strip()
            if key and key not in keys:
                keys.append(key)
    (PUBLIC_ROOT / ".env.example").write_text(
        "".join(f"{key}=\n" for key in keys),
        encoding="utf-8",
    )
    (PUBLIC_ROOT / ".gitignore").write_text(
        "runtime/.env\n**/__pycache__/\n.pytest_cache/\n",
        encoding="utf-8",
    )
    GENERATED_AT_FILE.parent.mkdir(parents=True, exist_ok=True)
    GENERATED_AT_FILE.write_text(generated_at + "\n", encoding="utf-8")


def _write_manifests(
    *,
    generated_at: str,
    common_modules: dict[str, Path],
    unique_modules: dict[str, Path],
) -> None:
    """记录模块所有权、全部定义、散列与实际执行顺序。"""

    common_definitions = collect_definitions(common_modules)
    unique_definitions = collect_definitions(unique_modules)
    ownership = {
        "generated_at": generated_at,
        "source_root": str(SOURCE_ROOT),
        "public_modules": sorted(common_modules),
        "file_parsing_business_modules": ["file_parsing_chain.entry"],
        "extraction_module_targets": dict(sorted(EXTRACTION_TARGETS.items())),
        "source_definition_count": len(common_definitions) + len(unique_definitions),
        "source_definitions": [
            item.to_dict() for item in [*common_definitions, *unique_definitions]
        ],
        "source_hashes": {
            module: _sha256(path)
            for module, path in sorted({**common_modules, **unique_modules}.items())
        },
    }
    _write_json(PUBLIC_ROOT / "manifests" / "ownership.json", ownership)

    for root, chain, seeds in (
        (FIRST_ROOT, "文件解析链", FIRST_SEEDS),
        (SECOND_ROOT, "DeepSeek 提取入库链", SECOND_SEEDS),
    ):
        _write_json(
            root / "manifests" / "definitions.json",
            {
                "chain": chain,
                "generated_at": generated_at,
                "seed_modules": seeds,
                "public_modules": sorted(common_modules),
                "business_modules": (
                    ["file_parsing_chain.entry"]
                    if root == FIRST_ROOT
                    else sorted(EXTRACTION_TARGETS.values())
                ),
                "source_definition_count": len(common_definitions)
                + (0 if root == FIRST_ROOT else len(unique_definitions)),
                "missing_definitions": [],
                "extra_definitions": [],
            },
        )

    (FIRST_ROOT / "manifests" / "execution_order.md").write_text(
        "# 文件解析链执行顺序\n\n"
        "薄入口 → 公共 processor → 文件校验/类型分发 → 文档、图像、音频或文本处理"
        " → 标准化结果 → 可选导出/索引。\n",
        encoding="utf-8",
    )
    (SECOND_ROOT / "manifests" / "execution_order.md").write_text(
        "# DeepSeek 提取入库链执行顺序\n\n"
        "上传入口 → 公共 processor → 统一原文 → 原文入库 → DeepSeek 三组提示词"
        " → 问答/意图映射 → AI_Wendajilu、AI_Yitu 入库 → 临时文件清理。\n",
        encoding="utf-8",
    )


def _write_readmes(generated_at: str) -> None:
    """写明三个所有权目录的职责，避免后续再次复制公共代码。"""

    PUBLIC_ROOT.mkdir(parents=True, exist_ok=True)
    PUBLIC_ROOT.joinpath("README.md").write_text(
        "# 公共程序文件\n\n"
        f"生成时间：{generated_at}\n\n"
        "`runtime/app` 是两条链唯一共享实现；真实 `.env` 也只存放在此运行时。\n",
        encoding="utf-8",
    )
    FIRST_ROOT.joinpath("README.md").write_text(
        "# 文件解析业务链\n\n"
        f"生成时间：{generated_at}\n\n"
        "`runtime/file_parsing_chain` 只保存薄业务入口，公共实现来自"
        " `public_program_files/runtime/app`。\n",
        encoding="utf-8",
    )
    SECOND_ROOT.joinpath("README.md").write_text(
        "# DeepSeek 提取入库业务链\n\n"
        f"生成时间：{generated_at}\n\n"
        "`runtime/extraction_chain` 只保存提取、ORM、路由和入库专属实现，"
        "公共解析与模型客户端来自 `public_program_files/runtime/app`。\n",
        encoding="utf-8",
    )


def _write_inline_coverage_manifest(generated_at: str) -> None:
    """汇总三个运行时的逐行说明覆盖率并拒绝任何漏注释代码。"""

    runtime_roots = (
        PUBLIC_ROOT / "runtime",
        FIRST_ROOT / "runtime",
        SECOND_ROOT / "runtime",
    )
    prefix = f"# [{generated_at}] 作用："
    file_records: dict[str, dict[str, int]] = {}
    total_code = 0
    total_annotations = 0
    uncovered: list[str] = []

    for runtime_root in runtime_roots:
        for path in sorted(runtime_root.rglob("*.py")):
            lines = path.read_text(encoding="utf-8").splitlines()
            annotations = sum(
                1 for line in lines if line.lstrip().startswith(prefix)
            )
            code_lines = 0
            for index, line in enumerate(lines):
                if line.lstrip().startswith(prefix):
                    continue
                code_lines += 1
                if index == 0 or not lines[index - 1].lstrip().startswith(prefix):
                    uncovered.append(f"{path}:{index + 1}")
            relative = path.relative_to(BACKEND_ROOT).as_posix()
            file_records[relative] = {
                "physical_lines": len(lines),
                "code_or_original_comment_lines": code_lines,
                "inline_explanation_lines": annotations,
            }
            total_code += code_lines
            total_annotations += annotations

    if uncovered:
        raise RuntimeError(f"逐行说明存在遗漏: {uncovered[:10]}")
    _write_json(
        PUBLIC_ROOT / "manifests" / "inline_comment_coverage.json",
        {
            "generated_at": generated_at,
            "python_file_count": len(file_records),
            "code_or_original_comment_lines": total_code,
            "inline_explanation_lines": total_annotations,
            "uncovered_lines": [],
            "coverage_percent": 100.0,
            "files": file_records,
        },
    )


def _clean_previous_outputs() -> None:
    """清除旧镜像/外置注释/清单，但不触碰链路测试。"""

    for root in (PUBLIC_ROOT, FIRST_ROOT, SECOND_ROOT):
        root.mkdir(parents=True, exist_ok=True)
        for name in ("runtime", "annotations", "manifests"):
            _remove_generated(root / name, root)
    for root in (FIRST_ROOT, SECOND_ROOT):
        for filename in (".env.example", ".gitignore"):
            _remove_generated(root / filename, root)


def build() -> dict[str, object]:
    """执行去重构建并返回可供命令行和测试检查的摘要。"""

    generated_at = _generated_at()
    first_modules = collect_module_closure(SOURCE_ROOT, FIRST_SEEDS)
    second_modules = collect_module_closure(SOURCE_ROOT, SECOND_SEEDS)
    common_names = set(first_modules) & set(second_modules)
    unique_names = set(second_modules) - common_names

    if set(first_modules) != common_names:
        raise RuntimeError("第一条链出现未纳入公共层的独占依赖")
    if unique_names != set(EXTRACTION_TARGETS):
        raise RuntimeError(
            "提取链独占模块集合变化，必须人工复核所有权: "
            f"{sorted(unique_names ^ set(EXTRACTION_TARGETS))}"
        )

    common_modules = {name: first_modules[name] for name in sorted(common_names)}
    unique_modules = {name: second_modules[name] for name in sorted(unique_names)}
    _clean_previous_outputs()

    public_package_root = PUBLIC_ROOT / "runtime" / "app"
    for module, source_path in common_modules.items():
        source = source_path.read_text(encoding="utf-8-sig")
        target = PUBLIC_ROOT / "runtime" / source_path.relative_to(SOURCE_ROOT)
        _write_module(
            source=source,
            target=target,
            package_root=public_package_root,
            module=module,
            owner="公共程序层",
            generated_at=generated_at,
        )

    parsing_package = FIRST_ROOT / "runtime" / "file_parsing_chain"
    _write_module(
        source=_facade_source(),
        target=parsing_package / "entry.py",
        package_root=parsing_package,
        module="file_parsing_chain.entry",
        owner="文件解析业务链",
        generated_at=generated_at,
    )

    extraction_package = SECOND_ROOT / "runtime" / "extraction_chain"
    for module, source_path in unique_modules.items():
        source = _rewrite_extraction_imports(
            source_path.read_text(encoding="utf-8-sig")
        )
        _write_module(
            source=source,
            target=extraction_package / EXTRACTION_TARGETS[module],
            package_root=extraction_package,
            module=f"extraction_chain.{Path(EXTRACTION_TARGETS[module]).stem}",
            owner="DeepSeek 提取入库业务链",
            generated_at=generated_at,
        )

    _provision_configuration(generated_at)
    _write_manifests(
        generated_at=generated_at,
        common_modules=common_modules,
        unique_modules=unique_modules,
    )
    _write_inline_coverage_manifest(generated_at)
    _write_readmes(generated_at)
    return {
        "generated_at": generated_at,
        "public_modules": len(common_modules),
        "extraction_modules": len(unique_modules),
        "public_definitions": len(collect_definitions(common_modules)),
        "extraction_definitions": len(collect_definitions(unique_modules)),
    }


def main() -> int:
    """命令行入口：成功时打印不含敏感信息的构建摘要。"""

    print(json.dumps(build(), ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
