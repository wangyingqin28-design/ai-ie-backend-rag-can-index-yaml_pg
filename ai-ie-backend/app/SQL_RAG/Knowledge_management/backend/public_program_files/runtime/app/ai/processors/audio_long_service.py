# [2026-07-03 18:11:51] 作用：导入依赖 `from pathlib import Path`，供 模块级初始化 使用；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
from pathlib import Path
# [2026-07-03 18:11:51] 作用：导入依赖 `import shutil`，供 模块级初始化 使用；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
import shutil
# [2026-07-03 18:11:51] 作用：导入依赖 `import subprocess`，供 模块级初始化 使用；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
import subprocess
# [2026-07-03 18:11:51] 作用：导入依赖 `import tempfile`，供 模块级初始化 使用；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
import tempfile
# [2026-07-03 18:11:51] 作用：导入依赖 `from .audio_service import transcribe_audio`，供 模块级初始化 使用；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
from .audio_service import transcribe_audio
# [2026-07-03 18:11:51] 作用：声明同步函数 check_ffmpeg_available，封装可复用的处理步骤；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 check_ffmpeg_available
def check_ffmpeg_available() -> None:
    # [2026-07-03 18:11:51] 作用：在 check_ffmpeg_available 中按条件 `if not shutil.which("ffmpeg"):` 选择执行分支；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 check_ffmpeg_available
    if not shutil.which("ffmpeg"):
        # [2026-07-03 18:11:51] 作用：在 check_ffmpeg_available 抛出 `raise RuntimeError(`，阻止无效状态继续传播；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 check_ffmpeg_available
        raise RuntimeError(
            # [2026-07-03 18:11:51] 作用：在 check_ffmpeg_available 中执行具体代码片段 `"未检测到 ffmpeg，请先安装 ffmpeg，并确保 ffmpeg 已加入系统 PATH。"`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 check_ffmpeg_available
            "未检测到 ffmpeg，请先安装 ffmpeg，并确保 ffmpeg 已加入系统 PATH。"
        # [2026-07-03 18:11:51] 作用：完善 同步函数 check_ffmpeg_available 的签名或多行表达式片段 `)`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 check_ffmpeg_available
        )
# [2026-07-03 18:11:51] 作用：声明同步函数 split_audio，封装可复用的处理步骤；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
def split_audio(
    # [2026-07-03 18:11:51] 作用：完善 同步函数 split_audio 的签名或多行表达式片段 `audio_path: str,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
    audio_path: str,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 split_audio 的签名或多行表达式片段 `chunk_seconds: int = 300,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
    chunk_seconds: int = 300,
# [2026-07-03 18:11:51] 作用：在 split_audio 中执行具体代码片段 `) -> list[Path]:`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
) -> list[Path]:
    # [2026-07-03 18:11:51] 作用：完善 同步函数 split_audio 的签名或多行表达式片段 `check_ffmpeg_available()`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
    check_ffmpeg_available()
    # [2026-07-03 18:11:51] 作用：为 audio_file 构造并保存赋值结果；本行执行 `audio_file = Path(audio_path)`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
    audio_file = Path(audio_path)
    # [2026-07-03 18:11:51] 作用：在 split_audio 中按条件 `if not audio_file.exists():` 选择执行分支；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
    if not audio_file.exists():
        # [2026-07-03 18:11:51] 作用：在 split_audio 抛出 `raise FileNotFoundError(f"音频文件不存在: {audio_path}")`，阻止无效状态继续传播；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")
    # [2026-07-03 18:11:51] 作用：为 temp_dir 构造并保存赋值结果；本行执行 `temp_dir = Path(tempfile.mkdtemp(prefix="audio_chunks_"))`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
    temp_dir = Path(tempfile.mkdtemp(prefix="audio_chunks_"))
    # [2026-07-03 18:11:51] 作用：为 output_pattern 构造并保存赋值结果；本行执行 `output_pattern = temp_dir / "chunk_%03d.wav"`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
    output_pattern = temp_dir / "chunk_%03d.wav"
    # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `command = [`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
    command = [
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `"ffmpeg",`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        "ffmpeg",
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `"-y",`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        "-y",
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `"-i",`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        "-i",
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `str(audio_file),`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        str(audio_file),
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `"-f",`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        "-f",
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `"segment",`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        "segment",
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `"-segment_time",`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        "-segment_time",
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `str(chunk_seconds),`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        str(chunk_seconds),
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `"-ar",`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        "-ar",
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `"16000",`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        "16000",
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `"-ac",`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        "-ac",
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `"1",`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        "1",
        # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `str(output_pattern),`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        str(output_pattern),
    # [2026-07-03 18:11:51] 作用：为 command 构造并保存赋值结果；本行执行 `]`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
    ]
    # [2026-07-03 18:11:51] 作用：在 split_audio 中执行具体代码片段 `subprocess.run(`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
    subprocess.run(
        # [2026-07-03 18:11:51] 作用：完善 同步函数 split_audio 的签名或多行表达式片段 `command,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        command,
        # [2026-07-03 18:11:51] 作用：完善 同步函数 split_audio 的签名或多行表达式片段 `check=True,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        check=True,
        # [2026-07-03 18:11:51] 作用：完善 同步函数 split_audio 的签名或多行表达式片段 `stdout=subprocess.DEVNULL,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        stdout=subprocess.DEVNULL,
        # [2026-07-03 18:11:51] 作用：完善 同步函数 split_audio 的签名或多行表达式片段 `stderr=subprocess.DEVNULL,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
        stderr=subprocess.DEVNULL,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 split_audio 的签名或多行表达式片段 `)`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
    )
    # [2026-07-03 18:11:51] 作用：从 split_audio 返回表达式 `return sorted(temp_dir.glob("chunk_*.wav"))` 的结果；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 split_audio
    return sorted(temp_dir.glob("chunk_*.wav"))
# [2026-07-03 18:11:51] 作用：声明异步函数 transcribe_long_audio，提供可等待的链路处理入口；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
async def transcribe_long_audio(
    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `audio_path: str,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
    audio_path: str,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `chunk_seconds: int = 300,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
    chunk_seconds: int = 300,
# [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中执行具体代码片段 `) -> dict:`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
) -> dict:
    # [2026-07-03 18:11:51] 作用：为 chunks 构造并保存赋值结果；本行执行 `chunks = split_audio(`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
    chunks = split_audio(
        # [2026-07-03 18:11:51] 作用：为 chunks 构造并保存赋值结果；本行执行 `audio_path=audio_path,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
        audio_path=audio_path,
        # [2026-07-03 18:11:51] 作用：为 chunks 构造并保存赋值结果；本行执行 `chunk_seconds=chunk_seconds,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
        chunk_seconds=chunk_seconds,
    # [2026-07-03 18:11:51] 作用：为 chunks 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
    )
    # [2026-07-03 18:11:51] 作用：为 temp_dir 构造并保存赋值结果；本行执行 `temp_dir = chunks[0].parent if chunks else None`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
    temp_dir = chunks[0].parent if chunks else None
    # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中用 `try:` 控制异常处理或资源清理；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
    try:
        # [2026-07-03 18:11:51] 作用：为 sections 构造并保存赋值结果；本行执行 `sections = []`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
        sections = []
        # [2026-07-03 18:11:51] 作用：为 results 构造并保存赋值结果；本行执行 `results = []`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
        results = []
        # [2026-07-03 18:11:51] 作用：为 transcription_model 构造并保存赋值结果；本行执行 `transcription_model = None`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
        transcription_model = None
        # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中通过 `for index, chunk_file in enumerate(chunks, start=1):` 迭代处理数据；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
        for index, chunk_file in enumerate(chunks, start=1):
            # [2026-07-03 18:11:51] 作用：为 start_seconds 构造并保存赋值结果；本行执行 `start_seconds = (index - 1) * chunk_seconds`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
            start_seconds = (index - 1) * chunk_seconds
            # [2026-07-03 18:11:51] 作用：为 end_seconds 构造并保存赋值结果；本行执行 `end_seconds = index * chunk_seconds`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
            end_seconds = index * chunk_seconds
            # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中用 `try:` 控制异常处理或资源清理；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
            try:
                # [2026-07-03 18:11:51] 作用：为 result 构造并保存赋值结果；本行执行 `result = await transcribe_audio(str(chunk_file))`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                result = await transcribe_audio(str(chunk_file))
                # [2026-07-03 18:11:51] 作用：为 text 构造并保存赋值结果；本行执行 `text = result.get("text", "")`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                text = result.get("text", "")
                # [2026-07-03 18:11:51] 作用：为 model 构造并保存赋值结果；本行执行 `model = result.get("model")`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                model = result.get("model")
                # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中按条件 `if model:` 选择执行分支；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                if model:
                    # [2026-07-03 18:11:51] 作用：为 transcription_model 构造并保存赋值结果；本行执行 `transcription_model = model`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    transcription_model = model
                # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中执行具体代码片段 `sections.append(`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                sections.append(
                    # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中执行具体代码片段 `f"## 分段 {index} [{start_seconds}s - {end_seconds}s]\n\n{text}"`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    f"## 分段 {index} [{start_seconds}s - {end_seconds}s]\n\n{text}"
                # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `)`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                )
                # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中执行具体代码片段 `results.append({`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                results.append({
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"success": True,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    "success": True,
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"index": index,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    "index": index,
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"start_seconds": start_seconds,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    "start_seconds": start_seconds,
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"end_seconds": end_seconds,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    "end_seconds": end_seconds,
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"text_length": len(text),`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    "text_length": len(text),
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"model": model,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    "model": model,
                # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `})`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                })
            # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中用 `except Exception as e:` 控制异常处理或资源清理；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
            except Exception as e:
                # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中执行具体代码片段 `sections.append(`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                sections.append(
                    # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中执行具体代码片段 `f"## 分段 {index} [{start_seconds}s - {end_seconds}s]\n\n转写失败：{e}"`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    f"## 分段 {index} [{start_seconds}s - {end_seconds}s]\n\n转写失败：{e}"
                # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `)`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                )
                # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中执行具体代码片段 `results.append({`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                results.append({
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"success": False,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    "success": False,
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"index": index,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    "index": index,
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"start_seconds": start_seconds,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    "start_seconds": start_seconds,
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"end_seconds": end_seconds,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    "end_seconds": end_seconds,
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"error": str(e),`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                    "error": str(e),
                # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `})`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
                })
        # [2026-07-03 18:11:51] 作用：为 full_text 构造并保存赋值结果；本行执行 `full_text = "\n\n".join(sections)`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
        full_text = "\n\n".join(sections)
        # [2026-07-03 18:11:51] 作用：从 transcribe_long_audio 返回表达式 `return {` 的结果；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
        return {
            # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"success": True,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
            "success": True,
            # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"audio_path": audio_path,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
            "audio_path": audio_path,
            # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"chunk_seconds": chunk_seconds,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
            "chunk_seconds": chunk_seconds,
            # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"chunk_count": len(chunks),`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
            "chunk_count": len(chunks),
            # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"text": full_text,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
            "text": full_text,
            # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"model": transcription_model,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
            "model": transcription_model,
            # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `"results": results,`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
            "results": results,
        # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中执行具体代码片段 `}`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
        }
    # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中用 `finally:` 控制异常处理或资源清理；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
    finally:
        # [2026-07-03 18:11:51] 作用：在 transcribe_long_audio 中按条件 `if temp_dir and temp_dir.exists():` 选择执行分支；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
        if temp_dir and temp_dir.exists():
            # [2026-07-03 18:11:51] 作用：完善 异步函数 transcribe_long_audio 的签名或多行表达式片段 `shutil.rmtree(temp_dir, ignore_errors=True)`；理由依据：源模块 app.ai.processors.audio_long_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 transcribe_long_audio
            shutil.rmtree(temp_dir, ignore_errors=True)
