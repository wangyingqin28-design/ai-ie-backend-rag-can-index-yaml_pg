"""生成两条业务执行链的自包含源码镜像、定义清单与逐行中文注释。"""

from __future__ import annotations

import ast
import hashlib
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Iterable


KNOWLEDGE_TOOL_ROOT = Path(__file__).resolve().parents[1]
if str(KNOWLEDGE_TOOL_ROOT) not in sys.path:
    sys.path.insert(0, str(KNOWLEDGE_TOOL_ROOT))

from tools.chain_inventory import collect_definitions, collect_module_closure


SOURCE_ROOT = Path(
    r"D:\wkt\getsoft---ai-erp-backend-feature-rag-new\getsoft---ai-erp-backend"
)
KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
FIRST_ROOT = KNOWLEDGE_ROOT / "backend/File_parsing/parsing_logic"
SECOND_ROOT = (
    KNOWLEDGE_ROOT
    / "backend/Extracting_parsed_content_based_on_relevant_prompts"
    / "Extraction_of_file_related_prompts"
)
FIRST_SEEDS = ["app.ai.processors.processor"]
SECOND_SEEDS = [
    "app.routers.vlm_router",
    "app.services.ai.extraction.process_service",
]
DAMAGED_BACKUP = (
    SOURCE_ROOT / "app/ai/processors/document_service.py.corrupt-20260703.bak"
)
RESTORED_DOCUMENT_SERVICE = SOURCE_ROOT / "app/ai/processors/document_service.py"
SOURCE_ENV = SOURCE_ROOT / ".env"


def _sha256(path: Path) -> str:
    """计算文件的 SHA256，不读取或输出其中的敏感文本。"""

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest().upper()


def _migration_time(chain_root: Path) -> str:
    """首次生成时记录到秒，重复生成时复用既有时间以保持产物稳定。"""

    manifest = chain_root / "manifests/definitions.json"
    if manifest.is_file():
        current = json.loads(manifest.read_text(encoding="utf-8"))
        generated_at = current.get("generated_at")
        if generated_at:
            return str(generated_at)
    return datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")


def _definition_spans(source: str) -> list[tuple[int, int, str, str]]:
    """返回每个定义覆盖的物理行区间，用于解释行的所属节点。"""

    tree = ast.parse(source)
    spans: list[tuple[int, int, str, str]] = []

    class Visitor(ast.NodeVisitor):
        def __init__(self) -> None:
            self.scope: list[str] = []

        def _visit_definition(self, node: ast.AST, name: str, kind: str) -> None:
            qualname = ".".join([*self.scope, name])
            spans.append((node.lineno, node.end_lineno or node.lineno, qualname, kind))
            self.scope.append(name)
            self.generic_visit(node)
            self.scope.pop()

        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            self._visit_definition(node, node.name, "类")

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self._visit_definition(node, node.name, "同步函数")

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self._visit_definition(node, node.name, "异步函数")

    Visitor().visit(tree)
    return spans


def _line_scope(
    line_number: int,
    spans: list[tuple[int, int, str, str]],
) -> tuple[str, str] | None:
    """选择覆盖当前行且范围最小的定义作为该行所属节点。"""

    candidates = [span for span in spans if span[0] <= line_number <= span[1]]
    if not candidates:
        return None
    start, end, qualname, kind = min(candidates, key=lambda item: item[1] - item[0])
    return qualname, kind


def _line_purpose(code: str) -> str:
    """根据源码形态给每个物理行生成稳定的中文作用说明。"""

    stripped = code.strip()
    if not stripped:
        return "空行，用于分隔逻辑块并保持源码层次。"
    if stripped.startswith("#"):
        return "原始中文或英文注释，记录实现意图、步骤或约束。"
    if stripped.startswith(("from ", "import ")):
        return "导入当前节点运行所需的标准库、第三方库或项目内依赖。"
    if stripped.startswith("@"):
        return "装饰器行，为下方类或函数注册框架行为或元数据。"
    if stripped.startswith("class "):
        return "定义类，封装该节点的数据结构或运行行为。"
    if stripped.startswith("async def "):
        return "定义异步函数，供异步文件处理或模型调用链等待执行。"
    if stripped.startswith("def "):
        return "定义同步函数，封装当前节点的独立处理步骤。"
    if stripped.startswith(("if ", "elif ", "else:")):
        return "条件分支，根据输入、文件类型或结果状态选择执行路径。"
    if stripped.startswith(("for ", "while ")):
        return "循环控制行，逐项处理文件、分片、记录或模型结果。"
    if stripped.startswith(("try:", "except ", "finally:")):
        return "异常控制行，保证错误回滚、隔离或资源清理。"
    if stripped.startswith(("with ", "async with ")):
        return "上下文管理行，限定文件、数据库会话或异步资源生命周期。"
    if stripped.startswith(("match ", "case ")):
        return "模式匹配行，根据配置值选择具体实现。"
    if stripped.startswith("return"):
        return "返回当前节点的标准化结果或中间处理结果。"
    if stripped.startswith("raise "):
        return "显式抛出异常，阻止无效输入或不可恢复状态继续传播。"
    if stripped.startswith(("\"\"\"", "'''")):
        return "文档字符串边界或内容，说明模块、类、函数的契约。"
    if "await " in stripped:
        return "等待异步下游节点完成，并接收其处理结果。"
    if "=" in stripped and "==" not in stripped and "!=" not in stripped:
        return "赋值或参数配置行，保存运行状态、常量或下游调用参数。"
    if stripped.endswith(("(", ",", "[", "{")):
        return "多行表达式的组成行，继续构造参数、集合或调用。"
    return "业务表达式或结构行，参与当前节点的数据处理与控制流程。"


def _annotation_rows(
    module: str,
    source: str,
    generated_at: str,
    seeds: Iterable[str],
) -> list[dict[str, str | int]]:
    """为源文件每个物理行生成一条中文说明记录。"""

    spans = _definition_spans(source)
    rows: list[dict[str, str | int]] = []
    seed_text = "、".join(seeds)

    for line_number, code in enumerate(source.splitlines(), start=1):
        scope = _line_scope(line_number, spans)
        if scope:
            qualname, kind = scope
            reason = (
                f"模块 {module} 位于入口 {seed_text} 的项目内传递依赖闭包；"
                f"本行属于{kind} {qualname}。"
            )
        else:
            reason = (
                f"模块 {module} 位于入口 {seed_text} 的项目内传递依赖闭包；"
                "本行属于模块初始化或模块级声明。"
            )

        rows.append(
            {
                "源行号": line_number,
                "迁移时间": generated_at,
                "作用": _line_purpose(code),
                "理由依据": reason,
                "原始代码": code,
            }
        )

    return rows


def _write_json(path: Path, data: object) -> None:
    """以稳定键序和 UTF-8 编码写入 JSON。"""

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def _write_jsonl(path: Path, rows: Iterable[dict[str, str | int]]) -> None:
    """逐行写入 JSON，确保一条记录严格对应一个源物理行。"""

    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(
        json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
        for row in rows
    )
    path.write_text(text, encoding="utf-8")


def _ensure_package_files(runtime_root: Path, target_file: Path, generated_at: str) -> None:
    """为私有 runtime/app 镜像补齐不会引入额外依赖的包标记文件。"""

    current = target_file.parent
    app_root = runtime_root / "app"
    while current == app_root or app_root in current.parents:
        init_file = current / "__init__.py"
        if not init_file.exists():
            init_file.write_text(
                f"# [{generated_at}] 中文说明：迁移镜像包标记，不包含业务逻辑。\n",
                encoding="utf-8",
            )
        if current == app_root:
            break
        current = current.parent


def _execution_order(chain_name: str, generated_at: str) -> str:
    """返回经源代码分析确认的业务执行顺序说明。"""

    common = f"""# {chain_name}执行顺序\n\n- 迁移时间：{generated_at}\n- 边界：项目内传递依赖全部纳入；第三方包内部实现排除。\n\n"""
    if chain_name == "文件解析链":
        return common + """## 主路径\n\n1. `processor.process_file` 调用 `file_utils.validate_file` 校验路径。\n2. `file_utils.get_file_type` 按扩展名选择 image/document/audio/text。\n3. 图片分支调用 `image_service.recognize_image` 或 `ocr_image`，最终经 `llm_client.chat_complete` 访问硅基流动视觉模型。\n4. 文档分支调用 `document_service.process_document_file`，再经 Docling 转换器输出 Markdown/JSON。\n5. 音频分支调用 `audio_long_service.transcribe_long_audio`，经 FFmpeg 分片后由 `audio_service.transcribe_audio` 访问硅基流动转录接口。\n6. 文本分支调用 `document_service.process_text_file` 读取 UTF-8 内容。\n7. 入口统一组装 success、file、engine、mode 与 result；可选调用 `export_service`。\n8. `process_folder` 扫描支持文件并逐个回到 `process_file`，单文件异常不会中断批次。\n9. `to_index_item` 把解析结构转换为可索引文本。\n10. Qdrant 包装入口延迟导入 `knowledge_index_service`，补充 kb/file/mode 元数据后调用 `vector_index_service.upsert_items_to_qdrant`。\n11. `config`、`vectorstore` 与 `query` 模块提供配置、连接器和查询数据结构。\n"""

    return common + """## 主路径\n\n1. `vlm_router.process_any_files` 接收 FastAPI 上传参数并调用 `process_service.process_uploaded_files`。\n2. 批量入口串行调用 `process_uploaded_file`；单文件先由 `_save_upload` 写入临时目录。\n3. `file_utils.get_file_type` 校验类型，随后调用完整文件解析链 `processor.process_file`。\n4. `_extract_raw_text` 按 document/text/audio/image 提取统一原文。\n5. `raw_data_service.save_raw_text` 分片并写入 `AI_YuanShishuju`，返回 `raw_data_id`。\n6. analyze/both 动作进入 `_run_fixed_audio_knowledge_extract`。\n7. `extract_audio_knowledge` 依次执行问答提取、问答 JSON 解析、描述生成、描述合并、意图提取和意图 JSON 解析。\n8. 所有模型请求经 `llm_client.llm_model_func` 和 `chat_complete` 访问硅基流动 DeepSeek。\n9. `qa_pair_service.save_qa_pairs` 映射截图字段并写入 `AI_Wendajilu`。\n10. `intent_service.save_intents` 写入 `AI_Yitu`，两表均通过 `Yssj_id` 关联原文。\n11. 可选调用 `export_service.export_knowledge_extract_result` 导出 raw/qa/intent Markdown。\n12. `finally` 无条件删除上传临时文件；路由返回原文、分析结果、数据库 ID 和可选解析详情。\n13. 解析链中的图片、文档、音频、Qdrant、配置和连接器依赖随本链一并镜像。\n"""


def provision_runtime_configuration(chain_roots: Iterable[Path]) -> None:
    """把记录配置原样复制为忽略文件，并生成不含值的示例配置。"""

    source_bytes = SOURCE_ENV.read_bytes()
    source_text = source_bytes.decode("utf-8-sig")
    key_names: list[str] = []
    for raw_line in source_text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key = line.split("=", 1)[0].strip()
        if key and key not in key_names:
            key_names.append(key)

    example_text = "".join(f"{key}=\n" for key in key_names)
    for chain_root in chain_roots:
        runtime_env = chain_root / "runtime/.env"
        runtime_env.parent.mkdir(parents=True, exist_ok=True)
        runtime_env.write_bytes(source_bytes)
        (chain_root / ".env.example").write_text(example_text, encoding="utf-8")


def build_chain(
    *,
    chain_name: str,
    chain_root: Path,
    seeds: list[str],
) -> dict[str, object]:
    """生成单条链的运行镜像、注释台账及三类审计清单。"""

    generated_at = _migration_time(chain_root)
    modules = collect_module_closure(SOURCE_ROOT, seeds)
    source_definitions = collect_definitions(modules)
    runtime_root = chain_root / "runtime"
    annotation_root = chain_root / "annotations"
    manifest_root = chain_root / "manifests"
    module_records: list[dict[str, object]] = []
    target_modules: dict[str, Path] = {}
    hashes: dict[str, dict[str, str]] = {}

    for module, source_path in modules.items():
        source = source_path.read_text(encoding="utf-8-sig")
        source_relative = source_path.relative_to(SOURCE_ROOT)
        target_path = runtime_root / source_relative
        annotation_path = annotation_root / source_relative.with_suffix(
            source_relative.suffix + ".lines.jsonl"
        )
        target_path.parent.mkdir(parents=True, exist_ok=True)
        provenance = (
            f"# [{generated_at}] 中文迁移说明：本文件完整复制自 {source_relative.as_posix()}；"
            f"纳入依据为 {chain_name} 的项目内传递依赖闭包。\n"
        )
        target_path.write_text(provenance + source, encoding="utf-8")
        _ensure_package_files(runtime_root, target_path, generated_at)

        rows = _annotation_rows(module, source, generated_at, seeds)
        _write_jsonl(annotation_path, rows)
        source_hash = _sha256(source_path)
        target_hash = _sha256(target_path)
        target_modules[module] = target_path
        module_records.append(
            {
                "module": module,
                "source_path": str(source_path),
                "source_relative": source_relative.as_posix(),
                "target_relative": target_path.relative_to(chain_root).as_posix(),
                "annotation_path": annotation_path.relative_to(chain_root).as_posix(),
                "source_line_count": len(source.splitlines()),
                "annotation_line_count": len(rows),
            }
        )
        hashes[module] = {
            "source_sha256": source_hash,
            "target_sha256": target_hash,
        }

    target_definitions = collect_definitions(target_modules)
    source_keys = {
        (item.module, item.qualname, item.kind) for item in source_definitions
    }
    target_keys = {
        (item.module, item.qualname, item.kind) for item in target_definitions
    }
    missing = sorted(source_keys - target_keys)
    extra = sorted(target_keys - source_keys)

    definitions_manifest: dict[str, object] = {
        "chain": chain_name,
        "generated_at": generated_at,
        "source_root": str(SOURCE_ROOT),
        "seed_modules": seeds,
        "module_count": len(modules),
        "modules": module_records,
        "source_definition_count": len(source_definitions),
        "target_definition_count": len(target_definitions),
        "source_definitions": [item.to_dict() for item in source_definitions],
        "target_definitions": [item.to_dict() for item in target_definitions],
        "missing_definitions": [list(item) for item in missing],
        "extra_definitions": [list(item) for item in extra],
    }
    hash_manifest = {
        "chain": chain_name,
        "generated_at": generated_at,
        "modules": hashes,
        "source_recovery": {
            "damaged_backup_path": str(DAMAGED_BACKUP),
            "damaged_backup_sha256": _sha256(DAMAGED_BACKUP),
            "restored_source_path": str(RESTORED_DOCUMENT_SERVICE),
            "restored_source_sha256": _sha256(RESTORED_DOCUMENT_SERVICE),
        },
    }
    _write_json(manifest_root / "definitions.json", definitions_manifest)
    _write_json(manifest_root / "source_hashes.json", hash_manifest)
    (manifest_root / "execution_order.md").write_text(
        _execution_order(chain_name, generated_at),
        encoding="utf-8",
    )
    (chain_root / ".gitignore").write_text(
        "runtime/.env\n**/__pycache__/\n.pytest_cache/\n",
        encoding="utf-8",
    )
    (chain_root / "README.md").write_text(
        f"# {chain_name}运行镜像\n\n"
        f"生成时间：{generated_at}\n\n"
        "- `runtime/app`：保持原 `app.*` 导入关系的完整项目内依赖镜像。\n"
        "- `annotations`：每个源物理行一条中文作用与依据说明。\n"
        "- `manifests`：执行顺序、全部 def/class 和 SHA256 证据。\n"
        "- `tests`：该链的隔离与真实集成测试。\n",
        encoding="utf-8",
    )
    return definitions_manifest


def main() -> int:
    """生成两条链，并以非零退出码拒绝任何定义缺失。"""

    results = [
        build_chain(
            chain_name="文件解析链",
            chain_root=FIRST_ROOT,
            seeds=FIRST_SEEDS,
        ),
        build_chain(
            chain_name="DeepSeek 提取入库链",
            chain_root=SECOND_ROOT,
            seeds=SECOND_SEEDS,
        ),
    ]
    provision_runtime_configuration([FIRST_ROOT, SECOND_ROOT])
    summary = [
        {
            "chain": result["chain"],
            "modules": result["module_count"],
            "definitions": result["source_definition_count"],
            "missing": len(result["missing_definitions"]),
            "extra": len(result["extra_definitions"]),
        }
        for result in results
    ]
    print(json.dumps(summary, ensure_ascii=False))
    return 1 if any(item["missing"] or item["extra"] for item in summary) else 0


if __name__ == "__main__":
    raise SystemExit(main())
