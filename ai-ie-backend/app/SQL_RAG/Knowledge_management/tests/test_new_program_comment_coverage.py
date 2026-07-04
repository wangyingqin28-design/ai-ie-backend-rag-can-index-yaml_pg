# [2026-07-04 10:18:20] 作用：导入正则表达式工具；理由依据：逐行审计需要严格识别日期到秒、作用和理由依据。
import re
# [2026-07-04 10:18:20] 作用：导入文件路径工具；理由依据：从 Knowledge 根目录枚举本次新增和修改的程序文件。
from pathlib import Path


# [2026-07-04 10:18:20] 作用：定位 Knowledge_management 根目录；理由依据：审计路径不能依赖调用测试时的工作目录。
KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
# [2026-07-04 10:18:20] 作用：定位 SQL_RAG 根目录；理由依据：本次修改的全量启动 PS1 位于 Knowledge 根目录的上一级。
SQL_RAG_ROOT = KNOWLEDGE_ROOT.parent
# [2026-07-04 10:18:20] 作用：声明 Python 中文逐行注释格式；理由依据：每条代码必须对应日期分秒、作用和理由依据。
PYTHON_ANNOTATION = re.compile(r"^\s*# \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] 作用：.+；理由依据：.+。$")
# [2026-07-04 10:18:20] 作用：声明 JavaScript 中文逐行注释格式；理由依据：前端新增程序采用同一审计合同。
JAVASCRIPT_ANNOTATION = re.compile(r"^\s*// \[\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}\] 作用：.+；理由依据：.+。$")
# [2026-07-04 10:18:20] 作用：列出本次需全量逐行审计的 Python 程序；理由依据：覆盖 API、真实验收器、WebUI 代理和对应回归测试。
PYTHON_FILES = [
    # [2026-07-04 10:18:20] 作用：纳入后端 API 应用；理由依据：健康、上传和真实调度入口属于新增生产程序。
    KNOWLEDGE_ROOT / "backend/knowledge_api/app.py",
    # [2026-07-04 10:18:20] 作用：纳入响应映射程序；理由依据：WebUI 卡片和返回主键由该模块生成。
    KNOWLEDGE_ROOT / "backend/knowledge_api/response_mapper.py",
    # [2026-07-04 10:18:20] 作用：纳入运行时路径初始化程序；理由依据：公共层和提取链去重后依赖该模块装配。
    KNOWLEDGE_ROOT / "backend/knowledge_api/runtime_paths.py",
    # [2026-07-04 10:18:20] 作用：纳入直接启动入口；理由依据：PS1 真实执行该文件启动 18320。
    KNOWLEDGE_ROOT / "backend/knowledge_api/run_server.py",
    # [2026-07-04 10:18:20] 作用：纳入 API 路由回归测试；理由依据：multipart 和健康合同必须保留逐行说明。
    KNOWLEDGE_ROOT / "backend/knowledge_api/tests/test_app.py",
    # [2026-07-04 10:18:20] 作用：纳入返回映射回归测试；理由依据：问答和意图卡片字段不能发生错位。
    KNOWLEDGE_ROOT / "backend/knowledge_api/tests/test_response_mapper.py",
    # [2026-07-04 10:18:20] 作用：纳入脚本直接执行回归测试；理由依据：防止再次出现 knowledge_api 包路径失败。
    KNOWLEDGE_ROOT / "backend/knowledge_api/tests/test_run_server.py",
    # [2026-07-04 10:18:20] 作用：纳入 WebUI HTTP 代理程序；理由依据：18321 通过该文件传递真实 multipart。
    KNOWLEDGE_ROOT / "webui/webui_server.py",
    # [2026-07-04 10:18:20] 作用：纳入 WebUI 代理字节级测试；理由依据：边界和正文必须原样转发。
    KNOWLEDGE_ROOT / "webui/tests/test_webui_proxy.py",
    # [2026-07-04 10:18:20] 作用：纳入真实保留记录验收器；理由依据：该工具负责第二轮外部 API 和三表逐列核验。
    KNOWLEDGE_ROOT / "tools/verify_full_stack_audio_ingestion.py",
    # [2026-07-04 10:18:20] 作用：纳入启动脚本静态合同测试；理由依据：新端口、进程和 ready 条件不能遗漏。
    KNOWLEDGE_ROOT / "tests/test_full_stack_launcher.py",
    # [2026-07-04 10:18:20] 作用：纳入验收器安全合同测试；理由依据：禁止删除记录或泄露密钥和连接串。
    KNOWLEDGE_ROOT / "tests/test_verifier_contract.py",
]
# [2026-07-04 10:18:20] 作用：列出本次需逐行审计的 JavaScript 程序；理由依据：覆盖真实文件上传、页面错误状态和对应前端测试。
JAVASCRIPT_FILES = [
    # [2026-07-04 10:18:20] 作用：纳入 Knowledge 页面控制程序；理由依据：真实解析成功和失败状态在该文件切换。
    KNOWLEDGE_ROOT / "webui/src/app.mjs",
    # [2026-07-04 10:18:20] 作用：纳入真实 multipart service；理由依据：该文件替换了模拟解析回退。
    KNOWLEDGE_ROOT / "webui/src/knowledgeService.mjs",
    # [2026-07-04 10:18:20] 作用：纳入新增页面布局和错误状态测试；理由依据：页面必须展示真实失败而非完成状态。
    KNOWLEDGE_ROOT / "webui/tests/addPageLayout.test.mjs",
    # [2026-07-04 10:18:20] 作用：纳入 multipart 与错误传播测试；理由依据：前端请求合同属于执行链的一部分。
    KNOWLEDGE_ROOT / "webui/tests/knowledgeService.test.mjs",
]


# [2026-07-04 10:18:20] 作用：判断字符是否被反斜杠转义；理由依据：扫描模板字符串时不能把转义反引号误判为结束符。
def _count_unescaped_backticks(text: str) -> int:
    # [2026-07-04 10:18:20] 作用：初始化反引号计数；理由依据：奇数次反引号才改变模板字符串状态。
    count = 0
    # [2026-07-04 10:18:20] 作用：初始化前一字符转义状态；理由依据：连续字符需按顺序解释。
    escaped = False
    # [2026-07-04 10:18:20] 作用：遍历当前 JavaScript 物理行字符；理由依据：识别纯模板内容而不向 HTML 字符串插入注释。
    for character in text:
        # [2026-07-04 10:18:20] 作用：跳过被反斜杠转义的当前字符；理由依据：该字符不能作为模板边界。
        if escaped:
            # [2026-07-04 10:18:20] 作用：清除一次性转义标志；理由依据：转义只影响紧随其后的一个字符。
            escaped = False
            # [2026-07-04 10:18:20] 作用：继续处理后续字符；理由依据：当前字符已经确定不参与边界计数。
            continue
        # [2026-07-04 10:18:20] 作用：识别反斜杠并标记下一字符；理由依据：避免把转义反引号算作模板结束。
        if character == "\\":
            # [2026-07-04 10:18:20] 作用：设置下一字符转义状态；理由依据：JavaScript 字符串使用反斜杠转义。
            escaped = True
            # [2026-07-04 10:18:20] 作用：继续处理后续字符；理由依据：反斜杠自身不是模板边界。
            continue
        # [2026-07-04 10:18:20] 作用：识别未转义反引号；理由依据：它会打开或关闭 JavaScript 模板字符串。
        if character == "`":
            # [2026-07-04 10:18:20] 作用：累加模板边界数量；理由依据：调用方依据奇偶性切换状态。
            count += 1
    # [2026-07-04 10:18:20] 作用：返回当前行未转义反引号数量；理由依据：JavaScript 审计据此排除纯 HTML 模板物理行。
    return count


# [2026-07-04 10:18:20] 作用：验证本次新增 Python 程序每条代码前恰有一条中文说明；理由依据：用户要求注释与代码同文件且不能多行说明对应一行代码。
def test_new_python_programs_have_one_comment_per_code_line() -> None:
    # [2026-07-04 10:18:20] 作用：初始化缺失或重复说明清单；理由依据：一次报告全部文件问题便于完整修正。
    failures: list[str] = []
    # [2026-07-04 10:18:20] 作用：遍历全部新增 Python 程序；理由依据：API、代理、验收和测试任何节点都不能漏审。
    for path in PYTHON_FILES:
        # [2026-07-04 10:18:20] 作用：断言目标文件存在；理由依据：文件被误删也属于验收失败。
        assert path.is_file(), path
        # [2026-07-04 10:18:20] 作用：以 UTF-8 读取可执行源码行；理由依据：中文说明不得乱码。
        lines = path.read_text(encoding="utf-8").splitlines()
        # [2026-07-04 10:18:20] 作用：逐行检查代码与说明邻接关系；理由依据：禁止把说明集中到其他文件或隔行放置。
        for index, line in enumerate(lines):
            # [2026-07-04 10:18:20] 作用：跳过空行和注释本身；理由依据：审计对象是可执行代码物理行。
            if not line.strip() or line.lstrip().startswith("#"):
                # [2026-07-04 10:18:20] 作用：继续检查下一物理行；理由依据：当前行不需要额外说明。
                continue
            # [2026-07-04 10:18:20] 作用：验证代码前一行匹配完整中文说明格式；理由依据：每条代码只能由紧邻说明解释。
            if index == 0 or not PYTHON_ANNOTATION.match(lines[index - 1]):
                # [2026-07-04 10:18:20] 作用：记录缺失说明的精确位置；理由依据：修正时不能遗漏任何代码行。
                failures.append(f"{path}:{index + 1}: 缺少紧邻中文说明")
            # [2026-07-04 10:18:20] 作用：检测一条代码前出现两条生成说明；理由依据：避免再次出现用户截图中的多行注释堆叠。
            elif index >= 2 and PYTHON_ANNOTATION.match(lines[index - 2]):
                # [2026-07-04 10:18:20] 作用：记录重复说明位置；理由依据：要求严格一条代码对应一条说明。
                failures.append(f"{path}:{index + 1}: 存在多条连续说明")
    # [2026-07-04 10:18:20] 作用：断言所有新增 Python 程序通过逐行审计；理由依据：任何失败都阻止最终完成报告。
    assert failures == []


# [2026-07-04 10:18:20] 作用：验证新增 JavaScript 可执行行逐行注释且不污染模板 HTML；理由依据：前端同样属于真实链路程序，但模板正文不是独立代码行。
def test_new_javascript_programs_have_one_comment_per_executable_line() -> None:
    # [2026-07-04 10:18:20] 作用：初始化 JavaScript 注释失败清单；理由依据：汇总所有文件和行号后统一修正。
    failures: list[str] = []
    # [2026-07-04 10:18:20] 作用：遍历真实上传前端及测试程序；理由依据：不能只注释 service 而漏掉页面状态或测试。
    for path in JAVASCRIPT_FILES:
        # [2026-07-04 10:18:20] 作用：读取 UTF-8 JavaScript 源码；理由依据：验证中文说明可正常解码。
        lines = path.read_text(encoding="utf-8").splitlines()
        # [2026-07-04 10:18:20] 作用：初始化模板字符串状态；理由依据：纯 HTML 模板行不能插入 JavaScript 单行注释。
        in_template = False
        # [2026-07-04 10:18:20] 作用：逐行扫描 JavaScript；理由依据：对每条模板外可执行代码执行邻接检查。
        for index, line in enumerate(lines):
            # [2026-07-04 10:18:20] 作用：在统计反引号前跳过空行和注释；理由依据：说明文字用反引号引用代码，但它不属于 JavaScript 模板边界。
            if not line.strip() or line.lstrip().startswith(("//", "/*", "*", "*/")):
                # [2026-07-04 10:18:20] 作用：继续扫描下一条可能执行的源码；理由依据：当前空行或注释不改变模板字符串状态。
                continue
            # [2026-07-04 10:18:20] 作用：保存当前行开始时的模板状态；理由依据：模板结束行仍属于字符串内容。
            starts_in_template = in_template
            # [2026-07-04 10:18:20] 作用：按当前行反引号奇偶切换模板状态；理由依据：下一行是否可执行由该状态决定。
            if _count_unescaped_backticks(line) % 2:
                # [2026-07-04 10:18:20] 作用：翻转模板字符串状态；理由依据：未转义边界成对打开和关闭模板。
                in_template = not in_template
            # [2026-07-04 10:18:20] 作用：跳过模板内部的纯字符串内容；理由依据：只审计模板外可执行代码且不向页面 HTML 插入注释。
            if starts_in_template:
                # [2026-07-04 10:18:20] 作用：继续扫描下一行；理由依据：当前行不要求 JavaScript 代码说明。
                continue
            # [2026-07-04 10:18:20] 作用：验证模板外代码前一行是完整中文说明；理由依据：每条真实执行语句必须有同文件邻接依据。
            if index == 0 or not JAVASCRIPT_ANNOTATION.match(lines[index - 1]):
                # [2026-07-04 10:18:20] 作用：记录缺失说明位置；理由依据：不得以测试通过掩盖注释遗漏。
                failures.append(f"{path}:{index + 1}: 缺少紧邻中文说明")
            # [2026-07-04 10:18:20] 作用：检测模板外代码前是否堆叠两条说明；理由依据：保持一行代码严格对应一条注释。
            elif index >= 2 and JAVASCRIPT_ANNOTATION.match(lines[index - 2]):
                # [2026-07-04 10:18:20] 作用：记录重复注释位置；理由依据：避免多行说明无法判断对应代码。
                failures.append(f"{path}:{index + 1}: 存在多条连续说明")
    # [2026-07-04 10:18:20] 作用：断言全部 JavaScript 可执行行注释合规；理由依据：前端真实上传链路也必须达到 100% 覆盖。
    assert failures == []


# [2026-07-04 10:18:20] 作用：验证 PS1 中所有新增 Knowledge 执行行都有同格式中文说明；理由依据：保留旧脚本已有内容，仅严格审计本次知识库集成区段。
def test_new_powershell_knowledge_lines_have_adjacent_comments() -> None:
    # [2026-07-04 10:18:20] 作用：读取全量启动脚本；理由依据：端口、进程、健康和最终 ready 均在该文件中。
    lines = (SQL_RAG_ROOT / "start-latest-full-stack.ps1").read_text(encoding="utf-8").splitlines()
    # [2026-07-04 10:18:20] 作用：初始化 PS1 注释失败清单；理由依据：报告所有新增 Knowledge 行的精确位置。
    failures: list[str] = []
    # [2026-07-04 10:18:20] 作用：遍历启动脚本全部物理行；理由依据：新增内容分布在变量、清理、启动、健康和输出多个区段。
    for index, line in enumerate(lines):
        # [2026-07-04 10:18:20] 作用：只选择含 Knowledge 标识的非注释代码行；理由依据：不强制改写用户已有主服务和资产类型脚本。
        if "knowledge" not in line.lower() or not line.strip() or line.lstrip().startswith("#"):
            # [2026-07-04 10:18:20] 作用：跳过非本次知识库集成代码；理由依据：避免覆盖工作树中与当前任务无关的既有修改。
            continue
        # [2026-07-04 10:18:20] 作用：验证新增 PS1 代码前是日期到秒的中文说明；理由依据：启动逻辑也必须说明作用和设计依据。
        if index == 0 or not PYTHON_ANNOTATION.match(lines[index - 1]):
            # [2026-07-04 10:18:20] 作用：记录 PS1 缺失注释位置；理由依据：最终审计不能遗漏任一知识库启动节点。
            failures.append(f"start-latest-full-stack.ps1:{index + 1}: 缺少紧邻中文说明")
    # [2026-07-04 10:18:20] 作用：断言所有新增 Knowledge PS1 行注释合规；理由依据：不合规时不得给出全部完成结论。
    assert failures == []
