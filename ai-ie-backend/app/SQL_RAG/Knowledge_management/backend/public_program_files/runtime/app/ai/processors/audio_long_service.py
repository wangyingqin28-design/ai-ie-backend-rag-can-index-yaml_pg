# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.audio_long_service 的模块级声明
from pathlib import Path
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.audio_long_service 的模块级声明
import shutil
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.audio_long_service 的模块级声明
import subprocess
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.audio_long_service 的模块级声明
import tempfile
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.audio_long_service 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.audio_long_service 的模块级声明
from .audio_service import transcribe_audio
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.audio_long_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.audio_long_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 check_ffmpeg_available
def check_ffmpeg_available() -> None:
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 check_ffmpeg_available
    if not shutil.which("ffmpeg"):
        # [2026-07-03 16:33:01] 作用：阻止无效状态继续传播；理由依据：公共程序层所有；本行属于同步函数 check_ffmpeg_available
        raise RuntimeError(
            # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 check_ffmpeg_available
            "未检测到 ffmpeg，请先安装 ffmpeg，并确保 ffmpeg 已加入系统 PATH。"
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 check_ffmpeg_available
        )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.audio_long_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.audio_long_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 split_audio
def split_audio(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
    audio_path: str,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 split_audio
    chunk_seconds: int = 300,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 split_audio
) -> list[Path]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 split_audio
    check_ffmpeg_available()
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 split_audio
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 split_audio
    audio_file = Path(audio_path)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 split_audio
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 split_audio
    if not audio_file.exists():
        # [2026-07-03 16:33:01] 作用：阻止无效状态继续传播；理由依据：公共程序层所有；本行属于同步函数 split_audio
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 split_audio
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 split_audio
    temp_dir = Path(tempfile.mkdtemp(prefix="audio_chunks_"))
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 split_audio
    output_pattern = temp_dir / "chunk_%03d.wav"
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 split_audio
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 split_audio
    command = [
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        "ffmpeg",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        "-y",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        "-i",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        str(audio_file),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        "-f",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        "segment",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        "-segment_time",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        str(chunk_seconds),
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        "-ar",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        "16000",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        "-ac",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        "1",
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        str(output_pattern),
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 split_audio
    ]
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 split_audio
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
    subprocess.run(
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于同步函数 split_audio
        command,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 split_audio
        check=True,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 split_audio
        stdout=subprocess.DEVNULL,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 split_audio
        stderr=subprocess.DEVNULL,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 split_audio
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 split_audio
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 split_audio
    return sorted(temp_dir.glob("chunk_*.wav"))
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.audio_long_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.audio_long_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
async def transcribe_long_audio(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
    audio_path: str,
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
    chunk_seconds: int = 300,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
) -> dict:
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
    chunks = split_audio(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        audio_path=audio_path,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        chunk_seconds=chunk_seconds,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
    )
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
    temp_dir = chunks[0].parent if chunks else None
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
    # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
    try:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        sections = []
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        results = []
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        transcription_model = None
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        # [2026-07-03 16:33:01] 作用：逐项处理集合或重复任务；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        for index, chunk_file in enumerate(chunks, start=1):
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            start_seconds = (index - 1) * chunk_seconds
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            end_seconds = index * chunk_seconds
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            try:
                # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                result = await transcribe_audio(str(chunk_file))
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                text = result.get("text", "")
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                model = result.get("model")
                # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                if model:
                    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    transcription_model = model
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                sections.append(
                    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    f"## 分段 {index} [{start_seconds}s - {end_seconds}s]\n\n{text}"
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                results.append({
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    "success": True,
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    "index": index,
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    "start_seconds": start_seconds,
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    "end_seconds": end_seconds,
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    "text_length": len(text),
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    "model": model,
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                })
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            except Exception as e:
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                sections.append(
                    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    f"## 分段 {index} [{start_seconds}s - {end_seconds}s]\n\n转写失败：{e}"
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                results.append({
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    "success": False,
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    "index": index,
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    "start_seconds": start_seconds,
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    "end_seconds": end_seconds,
                    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                    "error": str(e),
                # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
                })
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        full_text = "\n\n".join(sections)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        return {
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            "success": True,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            "audio_path": audio_path,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            "chunk_seconds": chunk_seconds,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            "chunk_count": len(chunks),
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            "text": full_text,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            "model": transcription_model,
            # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            "results": results,
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        }
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
    # [2026-07-03 16:33:01] 作用：控制异常处理和资源清理；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
    finally:
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
        if temp_dir and temp_dir.exists():
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于异步函数 transcribe_long_audio
            shutil.rmtree(temp_dir, ignore_errors=True)
