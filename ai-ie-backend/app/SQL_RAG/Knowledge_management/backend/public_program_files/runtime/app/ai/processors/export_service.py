# [2026-07-03 18:11:51] 作用：导入依赖 `from pathlib import Path`，供 模块级初始化 使用；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
from pathlib import Path
# [2026-07-03 18:11:51] 作用：声明同步函数 get_available_file_path，封装可复用的处理步骤；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
def get_available_file_path(file_path: Path) -> Path:
    # [2026-07-03 18:11:51] 作用：在 get_available_file_path 中执行具体代码片段 `"""如果文件已存在，自动生成不冲突的新文件名。"""`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
    """如果文件已存在，自动生成不冲突的新文件名。"""
    # [2026-07-03 18:11:51] 作用：在 get_available_file_path 中按条件 `if not file_path.exists():` 选择执行分支；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
    if not file_path.exists():
        # [2026-07-03 18:11:51] 作用：从 get_available_file_path 返回表达式 `return file_path` 的结果；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
        return file_path
    # [2026-07-03 18:11:51] 作用：为 stem 构造并保存赋值结果；本行执行 `stem = file_path.stem`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
    stem = file_path.stem
    # [2026-07-03 18:11:51] 作用：为 suffix 构造并保存赋值结果；本行执行 `suffix = file_path.suffix`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
    suffix = file_path.suffix
    # [2026-07-03 18:11:51] 作用：为 parent 构造并保存赋值结果；本行执行 `parent = file_path.parent`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
    parent = file_path.parent
    # [2026-07-03 18:11:51] 作用：为 index 构造并保存赋值结果；本行执行 `index = 1`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
    index = 1
    # [2026-07-03 18:11:51] 作用：在 get_available_file_path 中通过 `while True:` 迭代处理数据；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
    while True:
        # [2026-07-03 18:11:51] 作用：为 candidate 构造并保存赋值结果；本行执行 `candidate = parent / f"{stem}_{index}{suffix}"`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
        candidate = parent / f"{stem}_{index}{suffix}"
        # [2026-07-03 18:11:51] 作用：在 get_available_file_path 中按条件 `if not candidate.exists():` 选择执行分支；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
        if not candidate.exists():
            # [2026-07-03 18:11:51] 作用：从 get_available_file_path 返回表达式 `return candidate` 的结果；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
            return candidate
        # [2026-07-03 18:11:51] 作用：为 index 构造并保存赋值结果；本行执行 `index += 1`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 get_available_file_path
        index += 1
# [2026-07-03 18:11:51] 作用：声明同步函数 build_export_files，封装可复用的处理步骤；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_export_files
def build_export_files(*, file_path: str, output_dir: str) -> tuple[Path, Path]:
    # [2026-07-03 18:11:51] 作用：在 build_export_files 中执行具体代码片段 `"""根据源文件路径生成 raw 和 summary 的导出文件路径。"""`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_export_files
    """根据源文件路径生成 raw 和 summary 的导出文件路径。"""
    # [2026-07-03 18:11:51] 作用：为 output_path 构造并保存赋值结果；本行执行 `output_path = Path(output_dir)`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_export_files
    output_path = Path(output_dir)
    # [2026-07-03 18:11:51] 作用：完善 同步函数 build_export_files 的签名或多行表达式片段 `output_path.mkdir(parents=True, exist_ok=True)`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_export_files
    output_path.mkdir(parents=True, exist_ok=True)
    # [2026-07-03 18:11:51] 作用：为 source_path 构造并保存赋值结果；本行执行 `source_path = Path(file_path)`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_export_files
    source_path = Path(file_path)
    # [2026-07-03 18:11:51] 作用：为 stem 构造并保存赋值结果；本行执行 `stem = source_path.stem`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_export_files
    stem = source_path.stem
    # [2026-07-03 18:11:51] 作用：为 raw_file 构造并保存赋值结果；本行执行 `raw_file = get_available_file_path(output_path / f"{stem}_raw.md")`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_export_files
    raw_file = get_available_file_path(output_path / f"{stem}_raw.md")
    # [2026-07-03 18:11:51] 作用：为 summary_file 构造并保存赋值结果；本行执行 `summary_file = get_available_file_path(output_path / f"{stem}_summary.md")`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_export_files
    summary_file = get_available_file_path(output_path / f"{stem}_summary.md")
    # [2026-07-03 18:11:51] 作用：从 build_export_files 返回表达式 `return raw_file, summary_file` 的结果；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_export_files
    return raw_file, summary_file
# [2026-07-03 18:11:51] 作用：声明异步函数 export_processed_result，提供可等待的链路处理入口；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
async def export_processed_result(
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_processed_result 的签名或多行表达式片段 `*,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    *,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_processed_result 的签名或多行表达式片段 `processed: dict,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    processed: dict,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_processed_result 的签名或多行表达式片段 `raw_text: str,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    raw_text: str,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_processed_result 的签名或多行表达式片段 `output_dir: str,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    output_dir: str,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_processed_result 的签名或多行表达式片段 `summary_prompt: str | None = None,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    summary_prompt: str | None = None,
# [2026-07-03 18:11:51] 作用：在 export_processed_result 中执行具体代码片段 `) -> dict:`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
) -> dict:
    # [2026-07-03 18:11:51] 作用：在 export_processed_result 中执行具体代码片段 `"""导出统一解析结果；兼容 processor.py 传入的 summary_prompt 参数。"""`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    """导出统一解析结果；兼容 processor.py 传入的 summary_prompt 参数。"""
    # [2026-07-03 18:11:51] 作用：为 (raw_file, summary_file) 构造并保存赋值结果；本行执行 `raw_file, summary_file = build_export_files(`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    raw_file, summary_file = build_export_files(
        # [2026-07-03 18:11:51] 作用：为 (raw_file, summary_file) 构造并保存赋值结果；本行执行 `file_path=processed["file_path"],`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        file_path=processed["file_path"],
        # [2026-07-03 18:11:51] 作用：为 (raw_file, summary_file) 构造并保存赋值结果；本行执行 `output_dir=output_dir,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        output_dir=output_dir,
    # [2026-07-03 18:11:51] 作用：为 (raw_file, summary_file) 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    )
    # [2026-07-03 18:11:51] 作用：为 summary 构造并保存赋值结果；本行执行 `summary = summary_prompt or ""`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    summary = summary_prompt or ""
    # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `raw_content = "\n".join([`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    raw_content = "\n".join([
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `f"# {processed.get('file_name', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        f"# {processed.get('file_name', '')}",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `f"- file_type: {processed.get('file_type', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        f"- file_type: {processed.get('file_type', '')}",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `f"- engine: {processed.get('engine', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        f"- engine: {processed.get('engine', '')}",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `f"- source: {processed.get('file_path', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        f"- source: {processed.get('file_path', '')}",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `"---",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "---",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `raw_text or "未提取到有效内容。",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        raw_text or "未提取到有效内容。",
    # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `])`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    ])
    # [2026-07-03 18:11:51] 作用：为 summary_content 构造并保存赋值结果；本行执行 `summary_content = "\n".join([`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    summary_content = "\n".join([
        # [2026-07-03 18:11:51] 作用：为 summary_content 构造并保存赋值结果；本行执行 `f"# {processed.get('file_name', '')} AI 整理结果",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        f"# {processed.get('file_name', '')} AI 整理结果",
        # [2026-07-03 18:11:51] 作用：为 summary_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "",
        # [2026-07-03 18:11:51] 作用：为 summary_content 构造并保存赋值结果；本行执行 `f"- file_type: {processed.get('file_type', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        f"- file_type: {processed.get('file_type', '')}",
        # [2026-07-03 18:11:51] 作用：为 summary_content 构造并保存赋值结果；本行执行 `f"- engine: {processed.get('engine', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        f"- engine: {processed.get('engine', '')}",
        # [2026-07-03 18:11:51] 作用：为 summary_content 构造并保存赋值结果；本行执行 `f"- source: {processed.get('file_path', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        f"- source: {processed.get('file_path', '')}",
        # [2026-07-03 18:11:51] 作用：为 summary_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "",
        # [2026-07-03 18:11:51] 作用：为 summary_content 构造并保存赋值结果；本行执行 `"---",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "---",
        # [2026-07-03 18:11:51] 作用：为 summary_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "",
        # [2026-07-03 18:11:51] 作用：为 summary_content 构造并保存赋值结果；本行执行 `summary or "未启用 AI 分析，或未生成有效整理内容。",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        summary or "未启用 AI 分析，或未生成有效整理内容。",
    # [2026-07-03 18:11:51] 作用：为 summary_content 构造并保存赋值结果；本行执行 `])`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    ])
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_processed_result 的签名或多行表达式片段 `raw_file.write_text(raw_content, encoding="utf-8")`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    raw_file.write_text(raw_content, encoding="utf-8")
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_processed_result 的签名或多行表达式片段 `summary_file.write_text(summary_content, encoding="utf-8")`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    summary_file.write_text(summary_content, encoding="utf-8")
    # [2026-07-03 18:11:51] 作用：从 export_processed_result 返回表达式 `return {` 的结果；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    return {
        # [2026-07-03 18:11:51] 作用：完善 异步函数 export_processed_result 的签名或多行表达式片段 `"raw_output_file": str(raw_file),`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "raw_output_file": str(raw_file),
        # [2026-07-03 18:11:51] 作用：完善 异步函数 export_processed_result 的签名或多行表达式片段 `"summary_output_file": str(summary_file),`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "summary_output_file": str(summary_file),
        # [2026-07-03 18:11:51] 作用：完善 异步函数 export_processed_result 的签名或多行表达式片段 `"raw_text_length": len(raw_text or ""),`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "raw_text_length": len(raw_text or ""),
        # [2026-07-03 18:11:51] 作用：完善 异步函数 export_processed_result 的签名或多行表达式片段 `"summary_length": len(summary),`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "summary_length": len(summary),
        # [2026-07-03 18:11:51] 作用：完善 异步函数 export_processed_result 的签名或多行表达式片段 `"summary": summary,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
        "summary": summary,
    # [2026-07-03 18:11:51] 作用：在 export_processed_result 中执行具体代码片段 `}`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_processed_result
    }
# [2026-07-03 18:11:51] 作用：声明异步函数 export_knowledge_extract_result，提供可等待的链路处理入口；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
async def export_knowledge_extract_result(
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `*,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    *,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `processed: dict,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    processed: dict,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `raw_text: str,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    raw_text: str,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `output_dir: str,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    output_dir: str,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `qa_analysis: str | None = None,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    qa_analysis: str | None = None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `intent_analysis: str | None = None,`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    intent_analysis: str | None = None,
# [2026-07-03 18:11:51] 作用：在 export_knowledge_extract_result 中执行具体代码片段 `) -> dict:`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
) -> dict:
    # [2026-07-03 18:11:51] 作用：在 export_knowledge_extract_result 中执行具体代码片段 `"""将文件解析结果拆分导出为 raw、qa、intent 三个 Markdown 文件。"""`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    """将文件解析结果拆分导出为 raw、qa、intent 三个 Markdown 文件。"""
    # [2026-07-03 18:11:51] 作用：为 output_path 构造并保存赋值结果；本行执行 `output_path = Path(output_dir)`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    output_path = Path(output_dir)
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `output_path.mkdir(parents=True, exist_ok=True)`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    output_path.mkdir(parents=True, exist_ok=True)
    # [2026-07-03 18:11:51] 作用：为 source_path 构造并保存赋值结果；本行执行 `source_path = Path(processed["file_path"])`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    source_path = Path(processed["file_path"])
    # [2026-07-03 18:11:51] 作用：为 stem 构造并保存赋值结果；本行执行 `stem = source_path.stem`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    stem = source_path.stem
    # [2026-07-03 18:11:51] 作用：为 raw_file 构造并保存赋值结果；本行执行 `raw_file = get_available_file_path(output_path / f"{stem}_raw.md")`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    raw_file = get_available_file_path(output_path / f"{stem}_raw.md")
    # [2026-07-03 18:11:51] 作用：为 qa_file 构造并保存赋值结果；本行执行 `qa_file = get_available_file_path(output_path / f"{stem}_qa.md")`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    qa_file = get_available_file_path(output_path / f"{stem}_qa.md")
    # [2026-07-03 18:11:51] 作用：为 intent_file 构造并保存赋值结果；本行执行 `intent_file = get_available_file_path(output_path / f"{stem}_intent.md")`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    intent_file = get_available_file_path(output_path / f"{stem}_intent.md")
    # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `raw_content = "\n".join([`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    raw_content = "\n".join([
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `f"# {processed.get('file_name', '')} 原始解析结果",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        f"# {processed.get('file_name', '')} 原始解析结果",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `f"- file_type: {processed.get('file_type', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        f"- file_type: {processed.get('file_type', '')}",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `f"- engine: {processed.get('engine', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        f"- engine: {processed.get('engine', '')}",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `f"- source: {processed.get('file_path', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        f"- source: {processed.get('file_path', '')}",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `"---",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "---",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "",
        # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `raw_text or "未提取到有效内容。",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        raw_text or "未提取到有效内容。",
    # [2026-07-03 18:11:51] 作用：为 raw_content 构造并保存赋值结果；本行执行 `])`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    ])
    # [2026-07-03 18:11:51] 作用：为 qa_content 构造并保存赋值结果；本行执行 `qa_content = "\n".join([`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    qa_content = "\n".join([
        # [2026-07-03 18:11:51] 作用：为 qa_content 构造并保存赋值结果；本行执行 `f"# {processed.get('file_name', '')} 问答提取结果",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        f"# {processed.get('file_name', '')} 问答提取结果",
        # [2026-07-03 18:11:51] 作用：为 qa_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "",
        # [2026-07-03 18:11:51] 作用：为 qa_content 构造并保存赋值结果；本行执行 `f"- file_type: {processed.get('file_type', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        f"- file_type: {processed.get('file_type', '')}",
        # [2026-07-03 18:11:51] 作用：为 qa_content 构造并保存赋值结果；本行执行 `f"- engine: {processed.get('engine', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        f"- engine: {processed.get('engine', '')}",
        # [2026-07-03 18:11:51] 作用：为 qa_content 构造并保存赋值结果；本行执行 `f"- source: {processed.get('file_path', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        f"- source: {processed.get('file_path', '')}",
        # [2026-07-03 18:11:51] 作用：为 qa_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "",
        # [2026-07-03 18:11:51] 作用：为 qa_content 构造并保存赋值结果；本行执行 `"---",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "---",
        # [2026-07-03 18:11:51] 作用：为 qa_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "",
        # [2026-07-03 18:11:51] 作用：为 qa_content 构造并保存赋值结果；本行执行 `qa_analysis or "未生成问答提取结果。",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        qa_analysis or "未生成问答提取结果。",
    # [2026-07-03 18:11:51] 作用：为 qa_content 构造并保存赋值结果；本行执行 `])`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    ])
    # [2026-07-03 18:11:51] 作用：为 intent_content 构造并保存赋值结果；本行执行 `intent_content = "\n".join([`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    intent_content = "\n".join([
        # [2026-07-03 18:11:51] 作用：为 intent_content 构造并保存赋值结果；本行执行 `f"# {processed.get('file_name', '')} 意图提取结果",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        f"# {processed.get('file_name', '')} 意图提取结果",
        # [2026-07-03 18:11:51] 作用：为 intent_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "",
        # [2026-07-03 18:11:51] 作用：为 intent_content 构造并保存赋值结果；本行执行 `f"- file_type: {processed.get('file_type', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        f"- file_type: {processed.get('file_type', '')}",
        # [2026-07-03 18:11:51] 作用：为 intent_content 构造并保存赋值结果；本行执行 `f"- engine: {processed.get('engine', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        f"- engine: {processed.get('engine', '')}",
        # [2026-07-03 18:11:51] 作用：为 intent_content 构造并保存赋值结果；本行执行 `f"- source: {processed.get('file_path', '')}",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        f"- source: {processed.get('file_path', '')}",
        # [2026-07-03 18:11:51] 作用：为 intent_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "",
        # [2026-07-03 18:11:51] 作用：为 intent_content 构造并保存赋值结果；本行执行 `"---",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "---",
        # [2026-07-03 18:11:51] 作用：为 intent_content 构造并保存赋值结果；本行执行 `"",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "",
        # [2026-07-03 18:11:51] 作用：为 intent_content 构造并保存赋值结果；本行执行 `intent_analysis or "未生成意图提取结果。",`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        intent_analysis or "未生成意图提取结果。",
    # [2026-07-03 18:11:51] 作用：为 intent_content 构造并保存赋值结果；本行执行 `])`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    ])
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `raw_file.write_text(raw_content, encoding="utf-8")`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    raw_file.write_text(raw_content, encoding="utf-8")
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `qa_file.write_text(qa_content, encoding="utf-8")`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    qa_file.write_text(qa_content, encoding="utf-8")
    # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `intent_file.write_text(intent_content, encoding="utf-8")`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    intent_file.write_text(intent_content, encoding="utf-8")
    # [2026-07-03 18:11:51] 作用：从 export_knowledge_extract_result 返回表达式 `return {` 的结果；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    return {
        # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `"raw_output_file": str(raw_file),`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "raw_output_file": str(raw_file),
        # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `"qa_output_file": str(qa_file),`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "qa_output_file": str(qa_file),
        # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `"intent_output_file": str(intent_file),`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "intent_output_file": str(intent_file),
        # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `"raw_text_length": len(raw_text or ""),`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "raw_text_length": len(raw_text or ""),
        # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `"qa_length": len(qa_analysis or ""),`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "qa_length": len(qa_analysis or ""),
        # [2026-07-03 18:11:51] 作用：完善 异步函数 export_knowledge_extract_result 的签名或多行表达式片段 `"intent_length": len(intent_analysis or ""),`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
        "intent_length": len(intent_analysis or ""),
    # [2026-07-03 18:11:51] 作用：在 export_knowledge_extract_result 中执行具体代码片段 `}`；理由依据：源模块 app.ai.processors.export_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 export_knowledge_extract_result
    }
