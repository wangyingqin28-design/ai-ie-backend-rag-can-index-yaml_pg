# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/ai/processors/export_service.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
from pathlib import Path


def get_available_file_path(file_path: Path) -> Path:
    """如果文件已存在，自动生成不冲突的新文件名。"""
    if not file_path.exists():
        return file_path

    stem = file_path.stem
    suffix = file_path.suffix
    parent = file_path.parent

    index = 1
    while True:
        candidate = parent / f"{stem}_{index}{suffix}"
        if not candidate.exists():
            return candidate
        index += 1


def build_export_files(*, file_path: str, output_dir: str) -> tuple[Path, Path]:
    """根据源文件路径生成 raw 和 summary 的导出文件路径。"""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    source_path = Path(file_path)
    stem = source_path.stem

    raw_file = get_available_file_path(output_path / f"{stem}_raw.md")
    summary_file = get_available_file_path(output_path / f"{stem}_summary.md")

    return raw_file, summary_file


async def export_processed_result(
    *,
    processed: dict,
    raw_text: str,
    output_dir: str,
    summary_prompt: str | None = None,
) -> dict:
    """导出统一解析结果；兼容 processor.py 传入的 summary_prompt 参数。"""
    raw_file, summary_file = build_export_files(
        file_path=processed["file_path"],
        output_dir=output_dir,
    )
    summary = summary_prompt or ""
    raw_content = "\n".join([
        f"# {processed.get('file_name', '')}",
        "",
        f"- file_type: {processed.get('file_type', '')}",
        f"- engine: {processed.get('engine', '')}",
        f"- source: {processed.get('file_path', '')}",
        "",
        "---",
        "",
        raw_text or "未提取到有效内容。",
    ])
    summary_content = "\n".join([
        f"# {processed.get('file_name', '')} AI 整理结果",
        "",
        f"- file_type: {processed.get('file_type', '')}",
        f"- engine: {processed.get('engine', '')}",
        f"- source: {processed.get('file_path', '')}",
        "",
        "---",
        "",
        summary or "未启用 AI 分析，或未生成有效整理内容。",
    ])
    raw_file.write_text(raw_content, encoding="utf-8")
    summary_file.write_text(summary_content, encoding="utf-8")
    return {
        "raw_output_file": str(raw_file),
        "summary_output_file": str(summary_file),
        "raw_text_length": len(raw_text or ""),
        "summary_length": len(summary),
        "summary": summary,
    }


async def export_knowledge_extract_result(
    *,
    processed: dict,
    raw_text: str,
    output_dir: str,
    qa_analysis: str | None = None,
    intent_analysis: str | None = None,
) -> dict:
    """将文件解析结果拆分导出为 raw、qa、intent 三个 Markdown 文件。"""

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    source_path = Path(processed["file_path"])
    stem = source_path.stem

    raw_file = get_available_file_path(output_path / f"{stem}_raw.md")
    qa_file = get_available_file_path(output_path / f"{stem}_qa.md")
    intent_file = get_available_file_path(output_path / f"{stem}_intent.md")

    raw_content = "\n".join([
        f"# {processed.get('file_name', '')} 原始解析结果",
        "",
        f"- file_type: {processed.get('file_type', '')}",
        f"- engine: {processed.get('engine', '')}",
        f"- source: {processed.get('file_path', '')}",
        "",
        "---",
        "",
        raw_text or "未提取到有效内容。",
    ])

    qa_content = "\n".join([
        f"# {processed.get('file_name', '')} 问答提取结果",
        "",
        f"- file_type: {processed.get('file_type', '')}",
        f"- engine: {processed.get('engine', '')}",
        f"- source: {processed.get('file_path', '')}",
        "",
        "---",
        "",
        qa_analysis or "未生成问答提取结果。",
    ])

    intent_content = "\n".join([
        f"# {processed.get('file_name', '')} 意图提取结果",
        "",
        f"- file_type: {processed.get('file_type', '')}",
        f"- engine: {processed.get('engine', '')}",
        f"- source: {processed.get('file_path', '')}",
        "",
        "---",
        "",
        intent_analysis or "未生成意图提取结果。",
    ])

    raw_file.write_text(raw_content, encoding="utf-8")
    qa_file.write_text(qa_content, encoding="utf-8")
    intent_file.write_text(intent_content, encoding="utf-8")

    return {
        "raw_output_file": str(raw_file),
        "qa_output_file": str(qa_file),
        "intent_output_file": str(intent_file),
        "raw_text_length": len(raw_text or ""),
        "qa_length": len(qa_analysis or ""),
        "intent_length": len(intent_analysis or ""),
    }
