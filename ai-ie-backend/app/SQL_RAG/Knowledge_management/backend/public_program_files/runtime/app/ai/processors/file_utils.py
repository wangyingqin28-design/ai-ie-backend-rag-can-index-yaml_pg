# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
from pathlib import Path
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
from app.config import Config
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
DOCUMENT_EXTENSIONS = {".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls"}
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
TEXT_EXTENSIONS = {".txt", ".md", ".csv", ".json"}
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
AUDIO_EXTENSIONS = {".mp3", ".wav", ".m4a", ".flac", ".aac", ".ogg"}
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
SUPPORTED_EXTENSIONS = IMAGE_EXTENSIONS | DOCUMENT_EXTENSIONS | TEXT_EXTENSIONS | AUDIO_EXTENSIONS
# [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
config = Config()
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 get_file_type
def get_file_type(file_path: str) -> str:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 get_file_type
    """根据文件后缀判断处理类型：image/document/text/unsupported。"""
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 get_file_type
    suffix = Path(file_path).suffix.lower()
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 get_file_type
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_file_type
    if suffix in IMAGE_EXTENSIONS:
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_file_type
        return "image"
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 get_file_type
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_file_type
    if suffix in DOCUMENT_EXTENSIONS:
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_file_type
        return "document"
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 get_file_type
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_file_type
    if suffix in TEXT_EXTENSIONS:
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_file_type
        return "text"
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 get_file_type
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_file_type
    if suffix in AUDIO_EXTENSIONS:
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_file_type
        return "audio"
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 get_file_type
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_file_type
    return "unsupported"
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 validate_file
def validate_file(file_path: str) -> Path:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 validate_file
    """校验单文件路径，防止把不存在的路径或文件夹传入处理流程。"""
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 validate_file
    file = Path(file_path)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 validate_file
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 validate_file
    if not file.exists():
        # [2026-07-03 16:33:01] 作用：阻止无效状态继续传播；理由依据：公共程序层所有；本行属于同步函数 validate_file
        raise FileNotFoundError(f"文件不存在: {file_path}")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 validate_file
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 validate_file
    if not file.is_file():
        # [2026-07-03 16:33:01] 作用：阻止无效状态继续传播；理由依据：公共程序层所有；本行属于同步函数 validate_file
        raise IsADirectoryError(f"不是有效文件: {file_path}")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 validate_file
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 validate_file
    return file
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于模块 app.ai.processors.file_utils 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
def get_supported_files(folder_path: str, recursive: bool = False) -> list[str]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
    """扫描文件夹并返回当前模块支持处理的文件列表。"""
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
    folder = Path(folder_path)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
    if not folder.exists():
        # [2026-07-03 16:33:01] 作用：阻止无效状态继续传播；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
        raise FileNotFoundError(f"文件夹不存在: {folder_path}")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
    if not folder.is_dir():
        # [2026-07-03 16:33:01] 作用：阻止无效状态继续传播；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
        raise NotADirectoryError(f"不是有效文件夹: {folder_path}")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
    pattern = "**/*" if recursive else "*"
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
    # recursive=True 时使用 **/* 递归子目录；否则只读取当前目录一层。
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
    return [
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
        str(file)
        # [2026-07-03 16:33:01] 作用：逐项处理集合或重复任务；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
        for file in folder.glob(pattern)
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
        if file.is_file() and file.suffix.lower() in SUPPORTED_EXTENSIONS
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：公共程序层所有；本行属于同步函数 get_supported_files
    ]
