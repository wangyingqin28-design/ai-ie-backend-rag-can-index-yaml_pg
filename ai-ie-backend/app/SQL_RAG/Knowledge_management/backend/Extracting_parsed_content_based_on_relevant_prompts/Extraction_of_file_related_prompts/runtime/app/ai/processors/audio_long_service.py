# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/ai/processors/audio_long_service.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
from pathlib import Path
import shutil
import subprocess
import tempfile

from .audio_service import transcribe_audio


def check_ffmpeg_available() -> None:
    if not shutil.which("ffmpeg"):
        raise RuntimeError(
            "未检测到 ffmpeg，请先安装 ffmpeg，并确保 ffmpeg 已加入系统 PATH。"
        )


def split_audio(
    audio_path: str,
    chunk_seconds: int = 300,
) -> list[Path]:
    check_ffmpeg_available()

    audio_file = Path(audio_path)

    if not audio_file.exists():
        raise FileNotFoundError(f"音频文件不存在: {audio_path}")

    temp_dir = Path(tempfile.mkdtemp(prefix="audio_chunks_"))
    output_pattern = temp_dir / "chunk_%03d.wav"

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(audio_file),
        "-f",
        "segment",
        "-segment_time",
        str(chunk_seconds),
        "-ar",
        "16000",
        "-ac",
        "1",
        str(output_pattern),
    ]

    subprocess.run(
        command,
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return sorted(temp_dir.glob("chunk_*.wav"))


async def transcribe_long_audio(
    audio_path: str,
    chunk_seconds: int = 300,
) -> dict:
    chunks = split_audio(
        audio_path=audio_path,
        chunk_seconds=chunk_seconds,
    )
    temp_dir = chunks[0].parent if chunks else None

    try:
        sections = []
        results = []

        for index, chunk_file in enumerate(chunks, start=1):
            start_seconds = (index - 1) * chunk_seconds
            end_seconds = index * chunk_seconds

            try:
                result = await transcribe_audio(str(chunk_file))
                text = result.get("text", "")

                sections.append(
                    f"## 分段 {index} [{start_seconds}s - {end_seconds}s]\n\n{text}"
                )

                results.append({
                    "success": True,
                    "index": index,
                    "start_seconds": start_seconds,
                    "end_seconds": end_seconds,
                    "text_length": len(text),
                })

            except Exception as e:
                sections.append(
                    f"## 分段 {index} [{start_seconds}s - {end_seconds}s]\n\n转写失败：{e}"
                )

                results.append({
                    "success": False,
                    "index": index,
                    "start_seconds": start_seconds,
                    "end_seconds": end_seconds,
                    "error": str(e),
                })

        full_text = "\n\n".join(sections)

        return {
            "success": True,
            "audio_path": audio_path,
            "chunk_seconds": chunk_seconds,
            "chunk_count": len(chunks),
            "text": full_text,
            "results": results,
        }

    finally:
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir, ignore_errors=True)
