# [2026-07-04 10:18:20] 作用：导入命令行参数解析器；理由依据：PS1 需传入隔离的 host 与新端口。
import argparse
# [2026-07-04 10:18:20] 作用：导入 Python site 路径工具；理由依据：Knowledge 虚拟环境缺 Uvicorn，需只补充根虚拟环境包路径。
import site
# [2026-07-04 10:18:20] 作用：导入序列类型；理由依据：启动函数支持测试传入参数列表。
from typing import Sequence
# [2026-07-04 10:18:20] 作用：导入运行时路径和根虚拟环境位置；理由依据：启动前统一配置依赖与业务模块。
from knowledge_api.runtime_paths import ROOT_VENV_SITE_PACKAGES, configure_runtime_paths

# [2026-07-04 10:18:20] 作用：声明命令行解析器构造函数；理由依据：保持启动参数可测试且不散落。
def build_arg_parser() -> argparse.ArgumentParser:
    # [2026-07-04 10:18:20] 作用：创建 Knowledge 服务参数解析器；理由依据：日志帮助信息应明确服务用途。
    parser = argparse.ArgumentParser(description="Start Knowledge Management backend.")
    # [2026-07-04 10:18:20] 作用：添加监听地址参数；理由依据：方案 A 默认仅绑定本机。
    parser.add_argument("--host", default="127.0.0.1")
    # [2026-07-04 10:18:20] 作用：添加监听端口参数；理由依据：默认使用用户确认的新端口 18320。
    parser.add_argument("--port", type=int, default=18320)
    # [2026-07-04 10:18:20] 作用：返回已配置解析器；理由依据：启动函数统一消费。
    return parser

# [2026-07-04 10:18:20] 作用：声明 Uvicorn 启动入口；理由依据：PS1 通过独立 Python 进程运行 Knowledge API。
def run_server(argv: Sequence[str] | None = None) -> int:
    # [2026-07-04 10:18:20] 作用：解析显式或系统命令行参数；理由依据：支持单元测试和真实 PS1 调用。
    args = build_arg_parser().parse_args(list(argv) if argv is not None else None)
    # [2026-07-04 10:18:20] 作用：验证根虚拟环境包目录存在；理由依据：缺少 Uvicorn 时应给出明确启动错误。
    if not ROOT_VENV_SITE_PACKAGES.is_dir():
        # [2026-07-04 10:18:20] 作用：报告缺失依赖目录；理由依据：避免模糊的模块导入失败。
        raise RuntimeError(f"根虚拟环境依赖目录不存在: {ROOT_VENV_SITE_PACKAGES}")
    # [2026-07-04 10:18:20] 作用：把根虚拟环境包追加到搜索路径；理由依据：保留 Knowledge 环境数据库驱动优先级，仅补充 Uvicorn。
    site.addsitedir(str(ROOT_VENV_SITE_PACKAGES))
    # [2026-07-04 10:18:20] 作用：配置公共与提取运行时；理由依据：Uvicorn 导入应用前必须能找到业务包和 .env。
    configure_runtime_paths()
    # [2026-07-04 10:18:20] 作用：延迟导入 Uvicorn；理由依据：必须先补充根虚拟环境 site-packages。
    import uvicorn
    # [2026-07-04 10:18:20] 作用：启动独立 FastAPI 服务；理由依据：使用字符串工厂路径支持 Uvicorn 正常加载应用。
    uvicorn.run("knowledge_api.app:app", host=args.host, port=args.port, reload=False)
    # [2026-07-04 10:18:20] 作用：在服务正常停止后返回成功码；理由依据：便于 PowerShell 进程管理。
    return 0

# [2026-07-04 10:18:20] 作用：检测脚本直接执行；理由依据：模块被测试导入时不得自动启动服务器。
if __name__ == "__main__":
    # [2026-07-04 10:18:20] 作用：执行启动入口并传递退出码；理由依据：PS1 通过文件路径直接运行本脚本。
    raise SystemExit(run_server())
