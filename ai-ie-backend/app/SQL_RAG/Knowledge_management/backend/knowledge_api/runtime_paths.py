# [2026-07-04 10:18:20] 作用：导入进程工作目录和环境操作；理由依据：公共配置通过 runtime/.env 加载密钥与数据库参数。
import os
# [2026-07-04 10:18:20] 作用：导入模块搜索路径控制；理由依据：需同时加载公共 app 包和专属 extraction_chain 包。
import sys
# [2026-07-04 10:18:20] 作用：导入路径对象；理由依据：从当前文件稳定计算所有运行目录。
from pathlib import Path
# [2026-07-04 10:18:20] 作用：计算 Knowledge_management 根目录；理由依据：避免依赖外部启动目录。
KNOWLEDGE_ROOT = Path(__file__).resolve().parents[2]
# [2026-07-04 10:18:20] 作用：计算 Knowledge backend 根目录；理由依据：公共与提取运行时均位于该目录下。
BACKEND_ROOT = KNOWLEDGE_ROOT / "backend"
# [2026-07-04 10:18:20] 作用：定位公共运行时；理由依据：文件解析、配置、LLM 客户端只保留在 public_program_files。
PUBLIC_RUNTIME_ROOT = BACKEND_ROOT / "public_program_files" / "runtime"
# [2026-07-04 10:18:20] 作用：定位提取专属运行时；理由依据：总调度、ORM 和保存服务只保留在第二条业务链。
EXTRACTION_RUNTIME_ROOT = BACKEND_ROOT / "Extracting_parsed_content_based_on_relevant_prompts" / "Extraction_of_file_related_prompts" / "runtime"
# [2026-07-04 10:18:20] 作用：定位 ai-ie-backend 项目根目录；理由依据：Uvicorn 安装在仓库根虚拟环境而数据库驱动位于 Knowledge 虚拟环境。
PROJECT_ROOT = KNOWLEDGE_ROOT.parents[2]
# [2026-07-04 10:18:20] 作用：定位仓库根虚拟环境 site-packages；理由依据：启动器只需从该处补充缺失的 Uvicorn。
ROOT_VENV_SITE_PACKAGES = PROJECT_ROOT / ".venv" / "Lib" / "site-packages"

# [2026-07-04 10:18:20] 作用：声明运行时路径初始化函数；理由依据：API 导入前必须建立与原项目一致的模块和 .env 上下文。
def configure_runtime_paths() -> None:
    # [2026-07-04 10:18:20] 作用：验证公共运行时存在；理由依据：缺少公共解析链时应立即失败而非晚期 ImportError。
    if not PUBLIC_RUNTIME_ROOT.is_dir():
        # [2026-07-04 10:18:20] 作用：报告缺失公共运行时；理由依据：启动日志需要明确路径故障。
        raise RuntimeError(f"公共运行时不存在: {PUBLIC_RUNTIME_ROOT}")
    # [2026-07-04 10:18:20] 作用：验证提取运行时存在；理由依据：缺少专属保存链时不能启动假健康服务。
    if not EXTRACTION_RUNTIME_ROOT.is_dir():
        # [2026-07-04 10:18:20] 作用：报告缺失提取运行时；理由依据：启动日志需要明确路径故障。
        raise RuntimeError(f"提取运行时不存在: {EXTRACTION_RUNTIME_ROOT}")
    # [2026-07-04 10:18:20] 作用：逐个加入两类运行时路径；理由依据：避免复制公共模块回业务目录。
    for runtime_root in (PUBLIC_RUNTIME_ROOT, EXTRACTION_RUNTIME_ROOT):
        # [2026-07-04 10:18:20] 作用：把路径转换为模块搜索字符串；理由依据：sys.path 使用字符串条目。
        runtime_text = str(runtime_root)
        # [2026-07-04 10:18:20] 作用：避免重复插入同一路径；理由依据：测试重复导入不应持续污染 sys.path。
        if runtime_text not in sys.path:
            # [2026-07-04 10:18:20] 作用：把运行时加入模块搜索路径前端；理由依据：确保加载迁移后的目标代码而非其他同名包。
            sys.path.insert(0, runtime_text)
    # [2026-07-04 10:18:20] 作用：切换到含公共 .env 的目录；理由依据：Pydantic 配置使用相对 `.env` 路径加载真实密钥和连接。
    os.chdir(PUBLIC_RUNTIME_ROOT)
