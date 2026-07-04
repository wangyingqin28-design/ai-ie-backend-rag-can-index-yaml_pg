# [2026-07-04 10:18:20] 作用：导入模块搜索路径控制；理由依据：测试需从 Knowledge backend 根目录导入待建 API 包。
import sys
# [2026-07-04 10:18:20] 作用：导入路径对象；理由依据：根据测试文件位置稳定计算 backend 根目录。
from pathlib import Path
# [2026-07-04 10:18:20] 作用：计算 Knowledge backend 根目录；理由依据：避免依赖启动测试时的当前工作目录。
BACKEND_ROOT = Path(__file__).resolve().parents[2]
# [2026-07-04 10:18:20] 作用：把 backend 根目录放入模块搜索路径；理由依据：使 `knowledge_api` 可按正式包名导入。
sys.path.insert(0, str(BACKEND_ROOT))
