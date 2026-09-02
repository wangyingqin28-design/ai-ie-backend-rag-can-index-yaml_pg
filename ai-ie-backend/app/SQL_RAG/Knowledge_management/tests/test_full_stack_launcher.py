# [2026-07-31 10:46:00] 作用：导入 JSON 解析器；理由依据：双 profile 的门户来源和端口必须从唯一事实源验证。
import json
# [2026-09-02 14:41:08] 作用：导入子进程执行器；理由依据：固定网络 JSON 数组必须由 Windows PowerShell 5.1 实际执行验证，不能只做静态文本断言。
import subprocess
# [2026-07-04 10:18:20] 作用：导入路径对象；理由依据：从 Knowledge 测试目录稳定定位 SQL_RAG 启动脚本。
from pathlib import Path
# [2026-07-04 10:18:20] 作用：计算 Knowledge_management 根目录；理由依据：测试不能依赖当前工作目录。
KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
# [2026-07-04 10:18:20] 作用：定位 start-latest-full-stack.ps1；理由依据：Knowledge 根目录与脚本同属 SQL_RAG。
LAUNCHER = KNOWLEDGE_ROOT.parent / "start-latest-full-stack.ps1"
# [2026-08-03 18:46:02] 作用：定位共享 Compose 文件；理由依据：直连 Linux Engine 时 init bind 参数化必须与启动器原子验证。
COMPOSE = KNOWLEDGE_ROOT.parent / "docker-compose.yml"
# [2026-08-03 11:02:59] 作用：定位第二套服务器管理员原生固定入口；理由依据：V7管理员自调用递归与V8普通令牌假设都必须由独立回归测试永久阻断。
SERVER_LAUNCHER = KNOWLEDGE_ROOT.parent / "start-server-full-stack.ps1"
# [2026-08-04 08:34:00] 作用：定位第一套本地固定入口；理由依据：第二套管理员与Docker状态机变更必须由自动测试证明不会再次拦截local。
LOCAL_LAUNCHER = KNOWLEDGE_ROOT.parent / "start-local-full-stack.ps1"
# [2026-07-30 16:48:06] 作用：定位 Getsoft 正式启动适配器；理由依据：服务器第二套端口的数据库目标修复必须落在一键入口实际调用的文件。
GETSOFT_ADAPTER = KNOWLEDGE_ROOT.parent / "deployment" / "external_services" / "start-getsoft-ai-erp.ps1"
# [2026-07-31 10:46:01] 作用：定位双 profile 唯一事实源；理由依据：门户 CORS 与新服务器 IP 不得只存在于启动脚本文本。
PORT_PROFILES = KNOWLEDGE_ROOT.parent / "deployment" / "service-port-profiles.json"
# [2026-08-04 08:41:54] 作用：定位第二套独立profile；理由依据：随包基线策略必须由服务器自己的单profile事实源持有且不能写进第一套配置。
SERVER_PROFILE = KNOWLEDGE_ROOT.parent / "deployment" / "windows_workstation" / "server-second-ports-profile.json"
# [2026-08-31 18:21:57] 作用：定位商业服务共享启动器；理由依据：PgBouncer 私网修复必须同时受第一套兼容和第二套隔离合同约束。
COMMERCIAL_LAUNCHER = KNOWLEDGE_ROOT / "backend" / "large-scale_commercialization_upgrade" / "until" / "Start-KnowledgeCommercialServices.ps1"
# [2026-09-01 17:23:10] 作用：定位商业服务基础 Compose；理由依据：第二套固定网段必须通过运行时 override 注入且第一套成熟 YAML 保持不变。
COMMERCIAL_COMPOSE = KNOWLEDGE_ROOT / "backend" / "large-scale_commercialization_upgrade" / "until" / "docker-compose.commercial.yml"


# [2026-08-03 18:48:36] 作用：验证V12.3服务器入口允许管理员编排并声明第二套直连Engine与init路径合同；理由依据：HOTFIX2实机证明端点可用但Linux daemon仍拒绝Windows bind路径。
def test_server_launcher_separates_admin_entry_from_interactive_desktop() -> None:
    # [2026-08-03 10:00:49] 作用：读取用户实际执行的第二套固定入口；理由依据：包或文档修复不能替代正式脚本本身的合同。
    source = SERVER_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-03 10:00:50] 作用：禁止COM跨完整性级别转交；理由依据：ShellExecute在目标机继续保持管理员令牌并递归调用自身。
    assert "Shell.Application" not in source
    # [2026-08-03 10:00:51] 作用：禁止任何ShellExecute重启形式；理由依据：只替换COM对象名仍可能重现同一缺陷。
    assert ".ShellExecute(" not in source
    # [2026-08-03 10:00:52] 作用：禁止服务器入口获取自身路径后再执行；理由依据：固定入口无需递归，出现PSCommandPath即应阻断发布。
    assert "$PSCommandPath" not in source
    # [2026-08-03 11:03:07] 作用：禁止服务器入口创建任何替代PowerShell进程；理由依据：管理员原生模式必须在当前控制台直接进入共享引擎。
    assert "Start-Process" not in source
    # [2026-08-03 13:39:45] 作用：要求V10无副作用操作员探针存在；理由依据：安装器必须能动态确认管理员支持和零子进程结果。
    assert "ValidateOperatorContextOnly" in source
    # [2026-08-03 18:46:03] 作用：要求探针返回V12.3版本化合同；理由依据：HOTFIX2实机已证明直连端点可用但未覆盖Linux daemon的init bind路径合同。
    assert "server_operator_context_v12_3" in source
    # [2026-08-03 17:15:11] 作用：要求探针只声明管理员入口支持；理由依据：管理员负责系统配置和CLI但不再拥有Desktop直接启动许可。
    assert "SupportsAdministratorEntry=$true" in source
    # [2026-08-03 18:05:19] 作用：要求探针不再把Explorer请求冒充实际令牌测量；理由依据：截图已经证明该标签不能作为Docker API可用证据。
    assert "DockerDesktopLaunchMode='explorer_shell_execute_requested'" in source
    # [2026-08-03 18:05:20] 作用：要求探针固定第二套直连Linux Engine管道；理由依据：CLI和Compose必须绕过持续HTTP500的dockerDesktopLinuxEngine代理。
    assert "DockerCliEndpoint='npipe:////./pipe/docker_engine_linux'" in source
    # [2026-08-03 18:46:04] 作用：要求服务器入口声明init路径自动实测模式；理由依据：第二套不得再把Windows驱动器路径原样交给Linux daemon。
    assert "DockerInitBindMode='auto_probe_linux_vm_host_path'" in source
    # [2026-08-03 10:00:55] 作用：要求探针明确声明未创建子进程；理由依据：管理员安装验证不能再次产生窗口。
    assert "ChildProcessesStarted=0" in source
    # [2026-08-03 11:03:05] 作用：禁止入口继续保留管理员失败关闭分支；理由依据：V9第二条正式命令必须能在目标机管理员窗口直接运行。
    assert "if($isAdministrator){throw" not in source
    # [2026-08-03 17:15:13] 作用：要求服务器wrapper只标记第二套管理员编排入口；理由依据：不得重新授予管理员直接启动Docker Desktop的旧许可。
    assert "SQL_RAG_SERVER_ADMIN_ENTRY='1'" in source
    # [2026-08-03 17:15:14] 作用：禁止旧管理员Desktop许可残留；理由依据：V12缺陷不能通过兼容环境变量继续生效。
    assert "SQL_RAG_ALLOW_ADMIN_DESKTOP" not in source
    # [2026-08-03 18:05:21] 作用：要求服务器入口以进程级DOCKER_HOST注入独立端点；理由依据：不得修改用户全局context并影响第一套。
    assert "$env:DOCKER_HOST=$dockerEngineEndpoint" in source
    # [2026-08-03 18:05:22] 作用：要求服务器入口清除优先级更高的DOCKER_CONTEXT；理由依据：残留context会覆盖直连端点并悄悄回到Desktop代理。
    assert "Remove-Item Env:DOCKER_CONTEXT" in source


# [2026-08-04 08:34:01] 作用：验证两套固定入口持有互斥身份且管理员local不会进入第二套Docker状态机；理由依据：现场截图已证明仅认可服务器标记会在Docker检查前误伤第一套。
def test_local_and_server_fixed_entries_are_mutually_isolated() -> None:
    # [2026-08-04 08:34:02] 作用：读取第一套固定入口；理由依据：local身份必须在用户实际执行的wrapper内声明。
    local_source = LOCAL_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-04 08:34:03] 作用：读取第二套固定入口；理由依据：服务器入口必须主动清除local身份避免继承污染。
    server_source = SERVER_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-04 08:34:04] 作用：读取共享引擎；理由依据：管理员门禁与Docker分支的最终行为在此实现。
    engine_source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-04 08:34:05] 作用：断言第一套设置local标记并清除server标记；理由依据：一个进程不能同时获得两套运行身份。
    assert "SQL_RAG_LOCAL_ENTRY = '1'" in local_source and "Remove-Item Env:SQL_RAG_SERVER_ADMIN_ENTRY" in local_source
    # [2026-08-04 08:34:06] 作用：断言第二套设置server标记并清除local标记；理由依据：独立服务器合同不得继承本地权限。
    assert "SQL_RAG_SERVER_ADMIN_ENTRY='1'" in server_source and "Remove-Item Env:SQL_RAG_LOCAL_ENTRY" in server_source
    # [2026-08-04 08:34:07] 作用：断言共享门禁分别验证local与server身份；理由依据：管理员固定入口均应允许而直接调用共享引擎仍应拒绝。
    assert "$isLocalAdministratorEntry=" in engine_source and "not($isServerAdministratorEntry-or$isLocalAdministratorEntry)" in engine_source
    # [2026-08-04 08:34:08] 作用：断言第一套保留十分钟纯等待并在第二套120秒诊断前返回；理由依据：第二套直连管道和restart不得改变既有local启动策略。
    assert "if(-not$usesIndependentServiceProfile)" in engine_source and "Wait-DockerEngineReady -TimeoutSeconds 600" in engine_source
    # [2026-08-04 08:34:09] 作用：断言直连管道专用错误只在独立profile生效；理由依据：desktop-linux本地失败不能被错误报告为第二套docker_engine_linux故障。
    assert "if($usesIndependentServiceProfile-and$initialDockerFailureClassification-eq'direct_linux_engine_pipe_missing_or_unresponsive')" in engine_source


# [2026-08-06 10:17:36] 作用：验证看板数据库和原文地址均由当前profile单进程注入并运行态验收；理由依据：第二套曾返回28个第一套172.18.1.212链接。
def test_dashboard_dependencies_are_profile_injected_and_runtime_verified() -> None:
    # [2026-08-06 10:17:36] 作用：读取共享一键启动引擎；理由依据：第一套和第二套必须复用同一隔离实现并仅由profile取值。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-06 10:17:36] 作用：读取看板运行时组装代码；理由依据：禁止生产代码保留第一套IP默认值。
    runtime_source = (KNOWLEDGE_ROOT.parent / "Knowledge_Analysis" / "Customer_Risk_BusinessOpportunity_Perception_Dashboard" / "backend" / "dashboard_api" / "runtime.py").read_text(encoding="utf-8-sig")
    # [2026-08-06 10:17:36] 作用：断言看板数据库只在子进程创建窗口注入并恢复父环境；理由依据：后续Getsoft不得继承Knowledge连接串。
    assert "SetEnvironmentVariable('DATABASE_URL',$KnowledgeDatabaseUrl,'Process')" in source and "SetEnvironmentVariable('DATABASE_URL',$DashboardPreviousDatabaseUrl,'Process')" in source
    # [2026-08-06 10:17:36] 作用：断言看板原文入口来自当前profile并恢复父环境；理由依据：同一PowerShell连续启动两套时不得残留上一套地址。
    assert "SetEnvironmentVariable('CUSTOMER_RISK_KNOWLEDGE_BASE_URL',$KnowledgeMountedWebUrl,'Process')" in source and "SetEnvironmentVariable('CUSTOMER_RISK_KNOWLEDGE_BASE_URL',$DashboardPreviousKnowledgeBaseUrl,'Process')" in source
    # [2026-08-06 10:17:36] 作用：断言最终就绪合同包含独立profile门禁；理由依据：SELECT 1成功不能掩盖5432或172.18.1.212串线。
    assert "dashboard_profile_isolation=$dashboardDependencyReady" in source and "$dh.database.host" in source and "$dh.knowledgeBaseUrl" in source
    # [2026-08-06 10:17:36] 作用：禁止看板运行时再内置第一套主机；理由依据：缺配置必须失败关闭而不是跨机回退。
    assert '"http://172.18.1.212:18191/knowledgeManagement/"' not in runtime_source and "CUSTOMER_RISK_KNOWLEDGE_BASE_URL 未由当前部署profile注入" in runtime_source


# [2026-08-04 08:34:10] 作用：验证PowerShell 5.1全部网页健康探测采用非交互解析；理由依据：管理员窗口缺少IE首次配置时不能在最终验收阶段等待人工确认。
def test_webui_health_probes_never_prompt_for_ie_script_parsing() -> None:
    # [2026-08-04 08:34:11] 作用：读取共享引擎文本；理由依据：六个WebUI和Getsoft复验均由该文件执行。
    engine_source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-04 08:34:12] 作用：读取Getsoft适配器文本；理由依据：适配器内部还会独立验证Swagger页面。
    getsoft_source = GETSOFT_ADAPTER.read_text(encoding="utf-8-sig")
    # [2026-08-04 08:34:13] 作用：收集两份正式启动代码中的网页探测行；理由依据：任一遗漏都可能在一键执行中弹出交互提示。
    web_request_lines = [line for source in (engine_source, getsoft_source) for line in source.splitlines() if "Invoke-WebRequest" in line]
    # [2026-08-04 08:34:14] 作用：确认测试实际覆盖到网页探测；理由依据：空集合不能构成门禁证据。
    assert web_request_lines
    # [2026-08-04 08:34:15] 作用：要求每个网页探测都显式启用基础解析；理由依据：PowerShell 5.1只有该参数能消除IE脚本执行确认。
    assert all("-UseBasicParsing" in line for line in web_request_lines)


# [2026-08-04 08:41:55] 作用：验证第二套只校验随包基线且第一套仍保留原在线刷新策略；理由依据：截图中的重复在线克隆超时不能通过修改local行为来规避。
def test_server_packaged_clone_policy_is_independent_from_local_refresh() -> None:
    # [2026-08-04 08:41:56] 作用：读取共享引擎；理由依据：两种数据策略的唯一分流实现位于用户固定入口实际调用的文件。
    engine_source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-04 08:41:57] 作用：读取第二套独立profile；理由依据：测试必须证明策略来自服务器自己的配置而非IP或端口猜测。
    server_profile = json.loads(SERVER_PROFILE.read_text(encoding="utf-8-sig"))
    # [2026-08-04 08:41:58] 作用：断言第二套固定只使用校验后的随包基线；理由依据：新服务器不能再连接第一套权威源执行重复克隆。
    assert server_profile["data"]["clone_refresh_mode"] == "portable_seed_only"
    # [2026-08-04 08:41:59] 作用：断言第一套默认策略仍是在线刷新后回退；理由依据：本地已经跑通的数据更新行为必须原样保留。
    assert "$CloneRefreshMode='online_then_portable'" in engine_source
    # [2026-08-04 08:42:00] 作用：断言只有独立profile能够覆盖刷新策略；理由依据：第二套修复不得读取或写入本地双profile值。
    assert "if($usesIndependentServiceProfile){$CloneRefreshMode=" in engine_source
    # [2026-08-04 08:42:01] 作用：断言在线克隆调用被第一套策略条件包围；理由依据：portable_seed_only路径必须在执行clone_ai_erp前分流。
    assert "if($CloneRefreshMode-eq'online_then_portable'){" in engine_source
    # [2026-08-04 08:42:02] 作用：断言第二套成功输出确定基线结论；理由依据：已验证的数据包不能再被误报为权威源故障降级。
    assert "第二套随包数据基线已校验通过" in engine_source


# [2026-08-04 08:42:03] 作用：验证Getsoft数据库URL不再调用可空Uri中间对象；理由依据：目标服务器已实证InvokeMethodOnNull会中断28520启动。
def test_getsoft_database_url_rebuild_is_null_safe_and_profile_pinned() -> None:
    # [2026-08-04 08:42:04] 作用：读取正式Getsoft适配器；理由依据：修复必须落在第二套一键启动真实调用的文件。
    source = GETSOFT_ADAPTER.read_text(encoding="utf-8-sig")
    # [2026-08-04 08:42:05] 作用：禁止继续调用可空Uri对象的GetComponents；理由依据：该调用是截图中InvokeMethodOnNull的确定风险点。
    assert "$PinnedDatabaseUri.GetComponents" not in source
    # [2026-08-04 08:42:06] 作用：要求直接使用已构造完成的UriBuilder；理由依据：Builder已持有当前profile主机、端口和转义凭据且不依赖可空中间值。
    assert "$PinnedDatabaseUrl=[string]$PinnedDatabaseUriBuilder.ToString()" in source
    # [2026-08-04 08:42:07] 作用：要求回读验证当前profile主机和端口；理由依据：修空对象时不能让Getsoft重新串回第一套krauss或5432。
    assert "$PinnedDatabaseRoundTrip.Host-ne$ResolvedDatabaseIPv4[0].IPAddressToString" in source
    # [2026-08-04 08:42:08] 作用：要求回读端口等于第二套迁移库端口；理由依据：数据库连接串必须持续消费server_second_ports的25434。
    assert "$PinnedDatabaseRoundTrip.Port-ne$PinnedDatabasePort" in source


# [2026-08-18 13:06:07] 作用：验证本地既有 Getsoft 管理员进程在强归属预检后不会先阻塞于 UAC；理由依据：固定入口曾等待用户取消提权后才进入复用分支并以四项 Getsoft false 退出。
def test_local_getsoft_reuse_preflight_avoids_uac_without_weakening_server_replacement() -> None:
    # [2026-08-18 13:06:07] 作用：读取共享一键启动引擎；理由依据：本地预检、profile 隔离和最终严格复验都在正式父入口执行。
    engine_source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-18 13:06:07] 作用：读取 Getsoft 正式适配器；理由依据：跳过提权开关必须在 RunAs 之前 fail-closed。
    adapter_source = GETSOFT_ADAPTER.read_text(encoding="utf-8-sig")
    # [2026-08-18 13:06:07] 作用：断言无提权预检只允许第一套 local profile；理由依据：第二套永久离线服务器仍须由管理员入口确定性替换。
    assert "if($DeploymentProfile-eq'local'){" in engine_source
    # [2026-08-18 13:06:07] 作用：断言预检同时核对项目身份、真实监听和源码时效；理由依据：仅端口存活不能授权复用未知或陈旧进程。
    assert all(marker in engine_source for marker in ("$getsoftPreflightIdentityReady", "$getsoftPreflightListener", "$getsoftPreflightFreshReady"))
    # [2026-08-18 13:06:07] 作用：断言父入口只按完整预检结果注入单次跳过提权开关；理由依据：未通过预检时必须保持原适配器替换行为。
    assert "if($getsoftReusePreflightReady){'1'}else{$null}" in engine_source
    # [2026-08-18 13:06:07] 作用：断言适配器在 RunAs 前消费跳过提权开关；理由依据：检查位置晚于 Start-Process 会再次等待 UAC。
    assert adapter_source.index("SQL_RAG_GETSOFT_SKIP_ELEVATED_STOP") < adapter_source.index("-Verb RunAs")
    # [2026-08-18 13:06:07] 作用：断言最终复用仍真实消费 SSE 并核对干净结束；理由依据：避免把无 UAC 等同于降低在线健康门禁。
    assert all(marker in engine_source for marker in ("$getsoftExistingSseProbeScript", "clean_eof-eq$true", "done-eq$true", "error-eq$false"))
    # [2026-08-18 13:06:07] 作用：断言严格时效列表不再包含未定义的旧环境文件变量；理由依据：空 LiteralPath 曾使完整复用分支在运行时必然失败。
    assert "$OwnerEnvFile" not in engine_source
    # [2026-08-18 13:26:59] 作用：断言两个时效集合只含业务进程加载的配置、依赖和环境文件；理由依据：生命周期适配器与探针更新应由真实在线门禁验收，不能制造必须 UAC 重启的循环依赖。
    assert "$getsoftPreflightFreshnessFiles=@($GetsoftConfigPath," in engine_source and "$getsoftFreshnessFiles=@($GetsoftConfigPath," in engine_source

# [2026-07-04 10:18:20] 作用：验证 Knowledge 前后端完整接入全量启动脚本；理由依据：用户只执行这一条 PS1 命令验收。
def test_full_stack_launcher_contains_knowledge_services_and_health_gates() -> None:
    # [2026-07-04 10:18:20] 作用：读取启动脚本文本；理由依据：静态检查端口、命令和 ready 条件不启动外部服务。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-07-04 10:18:20] 作用：声明必须存在的 Knowledge 集成标记；理由依据：覆盖端口、进程、日志和健康链。
    required = (
        # [2026-07-30 11:38:00] 作用：要求知识后端端口来自统一部署配置；理由依据：本地与阿里云端口不能再由启动器中的散落常量分别维护。
        "$KnowledgeBackendPort=Get-ServiceProfilePort 'knowledge_backend'",
        # [2026-07-30 11:38:01] 作用：要求知识 WebUI 端口来自统一部署配置；理由依据：同一启动器必须按 local 或 aliyun profile 选择对应端口。
        "$KnowledgeWebPort=Get-ServiceProfilePort 'knowledge_web'",
        # [2026-07-04 10:18:20] 作用：要求启动 Knowledge API 入口；理由依据：真实后端必须由全量脚本拉起。
        "Knowledge_management\\backend\\knowledge_api\\run_server.py",
        # [2026-07-04 10:18:20] 作用：要求启动 Knowledge WebUI 入口；理由依据：用户需通过同源 `/api` 上传。
        "Knowledge_management\\webui\\webui_server.py",
        # [2026-07-04 10:18:20] 作用：要求后端日志前缀；理由依据：便于定位语音、DeepSeek 和数据库错误。
        "knowledge-backend-",
        # [2026-07-04 10:18:20] 作用：要求 WebUI 日志前缀；理由依据：便于定位代理错误。
        "knowledge-webui-",
        # [2026-07-04 10:18:20] 作用：要求后端 ready 状态变量；理由依据：最终成功条件必须包含真实 API 健康。
        "$knowledgeBackendReady",
        # [2026-07-04 10:18:20] 作用：要求 WebUI ready 状态变量；理由依据：最终成功条件必须包含页面可访问。
        "$knowledgeWebReady",
        # [2026-07-04 10:18:20] 作用：要求代理 ready 状态变量；理由依据：最终成功条件必须包含 `/api` 转发可用。
        "$knowledgeProxyReady",
        # [2026-07-04 10:18:20] 作用：要求 WebUI 代理健康路径；理由依据：确认 18321 能转发到 18320。
        "$KnowledgeWebUrl/api/health",
        # [2026-07-04 12:08:00] 作用：要求全量启动脚本包含前端语法门禁；理由依据：仅健康接口成功无法发现 app.mjs 语法错误导致的浏览器空白页。
        "node --check",
    # [2026-07-04 10:18:20] 作用：结束必需标记集合；理由依据：逐项检查缺失内容。
    )
    # [2026-07-04 10:18:20] 作用：遍历每个必需标记；理由依据：失败信息精确显示遗漏项。
    for marker in required:
        # [2026-07-04 10:18:20] 作用：断言标记存在于脚本；理由依据：任一缺失都不能宣称全量服务 ready。
        assert marker in source, marker
    # [2026-07-04 10:18:20] 作用：定位最终失败保护语句；理由依据：检查 all-ready 谓词而非仅变量声明。
    final_guard = source[source.rfind("if(!("):]
    # [2026-07-04 10:18:20] 作用：断言最终条件包含 Knowledge 后端；理由依据：后端失败时脚本必须抛错。
    assert "$knowledgeBackendReady" in final_guard
    # [2026-07-04 10:18:20] 作用：断言最终条件包含 Knowledge WebUI；理由依据：页面失败时脚本必须抛错。
    assert "$knowledgeWebReady" in final_guard
    # [2026-07-04 10:18:20] 作用：断言最终条件包含 Knowledge 代理；理由依据：代理失败时脚本必须抛错。
    assert "$knowledgeProxyReady" in final_guard


# [2026-07-30 11:29:00] 作用：验证固定一键入口启用并强制验收知识问答实时同步；理由依据：WebUI 保存到 PostgreSQL 后必须由同一启动链持续更新 Qdrant。
def test_full_stack_launcher_requires_knowledge_realtime_sync() -> None:
    # [2026-07-30 11:29:01] 作用：读取用户实际执行的共享一键启动引擎；理由依据：测试不能只约束临时命令或未被调用的辅助脚本。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-07-30 11:29:02] 作用：断言一键入口把外部源同步开关固定写为 true；理由依据：SQL_RAG .env 旧值为 false 时常驻同步器不会启动。
    assert "Set-EnvLine $EnvFile 'EXTERNAL_SOURCE_SYNC_ENABLED' 'true'" in source
    # [2026-07-30 11:29:03] 作用：断言健康检查读取 krauss_ai_ie_dev profile；理由依据：线程存在不能证明知识问答表首轮同步成功。
    assert "$knowledgeRealtimeSyncStatus.profiles.krauss_ai_ie_dev.ready" in source
    # [2026-07-30 11:29:04] 作用：断言全量等待条件包含实时同步门禁；理由依据：Qdrant 仍是旧内容时不得提前结束一键启动。
    assert "$dashboardProxyReady -and $knowledgeRealtimeSyncReady" in source
    # [2026-07-30 11:29:05] 作用：断言最终具名合同包含实时同步状态；理由依据：启动窗口和成功备份必须保留可审计结果。
    assert "knowledge_realtime_sync=$knowledgeRealtimeSyncReady" in source
    # [2026-07-30 11:31:01] 作用：断言成功备份元数据记录实时同步门禁；理由依据：恢复后的可运行基线不能遗漏双库联动证明。
    assert "'knowledge_realtime_sync'" in source


# [2026-07-13 09:18:00] 作用：验证克隆工具始终通过仓库绝对路径启动；理由依据：管理员 PowerShell 默认位于 System32，相对路径会错误解析到 C:\Windows\System32\app。
def test_full_stack_launcher_uses_absolute_clone_tool_paths() -> None:
    # [2026-07-13 09:18:00] 作用：读取正式全量启动脚本；理由依据：测试必须锁定用户实际执行的唯一入口。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-07-13 09:18:00] 作用：要求克隆脚本路径由 RepoRoot 拼接；理由依据：绝对路径不能受调用者当前工作目录影响。
    assert "$CloneAiErpScript=Join-Path $RepoRoot 'app\\SQL_RAG\\tools\\wkt_prasing_extra\\clone_ai_erp.py'" in source
    # [2026-07-13 09:18:00] 作用：要求校验脚本路径由 RepoRoot 拼接；理由依据：克隆成功后的结构复核必须具备相同路径稳定性。
    assert "$VerifyWktCloneScript=Join-Path $RepoRoot 'app\\SQL_RAG\\tools\\wkt_prasing_extra\\verify_clone.py'" in source
    # [2026-07-13 09:18:00] 作用：禁止继续使用旧相对路径调用；理由依据：该写法已在 System32 启动场景稳定复现截图中的找不到文件错误。
    assert "& $Py app\\SQL_RAG\\tools\\wkt_prasing_extra\\clone_ai_erp.py" not in source


# [2026-07-13 12:08:00] 作用：验证 Docker Compose 状态输出不会被全局 Stop 策略误判为启动失败；理由依据：Docker 在容器已运行时会把 Running 状态写入 stderr。
def test_full_stack_launcher_handles_docker_compose_stderr_by_exit_code() -> None:
    # [2026-07-13 12:08:00] 作用：读取用户实际执行的全量启动脚本；理由依据：回归测试必须约束唯一生产入口而非测试替身。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-07-13 12:08:00] 作用：要求脚本在 Docker 调用前暂时允许原生命令状态流；理由依据：PowerShell 5 会把 native stderr 包装成 ErrorRecord。
    assert "$ErrorActionPreference='Continue'" in source
    # [2026-07-13 12:08:00] 作用：要求脚本保存 Docker 真实退出码；理由依据：stderr 文本不等于失败，退出码才是 Compose 成败契约。
    assert "$composeExitCode=$LASTEXITCODE" in source
    # [2026-07-13 12:08:00] 作用：要求脚本按保存的退出码抛出真正异常；理由依据：兼容状态输出不能掩盖 Docker 的真实非零失败。
    assert "if($composeExitCode -ne 0)" in source


# [2026-07-08 14:18:33] 作用：验证启动脚本最终条件覆盖主业务脑、资产类型、知识库和统一挂载入口；理由依据：用户明确要求全量前后端服务一个都不能少。
def test_full_stack_launcher_final_guard_requires_all_services() -> None:
    # [2026-07-08 14:18:33] 作用：读取启动脚本文本；理由依据：最终 ready 判定是 PowerShell 静态合同，可不拉服务直接检查。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-07-08 14:18:33] 作用：截取最终失败保护语句；理由依据：只检查最终 throw 条件，不误判中间诊断输出。
    final_guard = source[source.rfind("if(!("):]
    # [2026-07-08 14:18:33] 作用：断言主业务脑后端是阻断条件；理由依据：主服务依赖污染时不能把全量服务误报为 ready。
    assert "$backendReady" in final_guard
    # [2026-07-08 14:18:33] 作用：断言主业务脑 WebUI 是阻断条件；理由依据：全量服务包含原有 18181 前端页面。
    assert "$webReady" in final_guard
    # [2026-07-08 14:18:33] 作用：断言主业务脑 WebUI 代理是阻断条件；理由依据：主前端同源代理失败时不算全量启动成功。
    assert "$proxyReady" in final_guard
    # [2026-07-08 14:18:33] 作用：断言资产后端仍是阻断条件；理由依据：资产类型管理页面和提示词维护依赖 18190 后端。
    assert "$assetBackendReady" in final_guard
    # [2026-07-08 14:18:33] 作用：断言资产 WebUI 仍是阻断条件；理由依据：外部挂载入口需要 18191 页面可访问。
    assert "$assetWebReady" in final_guard
    # [2026-07-08 14:18:33] 作用：断言资产 WebUI 代理仍是阻断条件；理由依据：资产页面 API 代理失败会导致资产下拉和提示词维护异常。
    assert "$assetProxyReady" in final_guard
    # [2026-07-08 14:18:33] 作用：断言知识库后端仍是阻断条件；理由依据：全景记录、编辑覆盖、纳入待审都依赖 18320 API。
    assert "$knowledgeBackendReady" in final_guard
    # [2026-07-08 14:18:33] 作用：断言知识库 WebUI 仍是阻断条件；理由依据：保留 18321 兼容入口时页面仍必须可访问。
    assert "$knowledgeWebReady" in final_guard
    # [2026-07-08 14:18:33] 作用：断言知识库 WebUI 代理仍是阻断条件；理由依据：保留 18321 兼容入口时 /api 健康必须可用。
    assert "$knowledgeProxyReady" in final_guard
    # [2026-07-08 14:18:33] 作用：断言资产挂载页面是阻断条件；理由依据：别人前端跳转资产类型使用 18191/resourceType/。
    assert "$assetMountedWebReady" in final_guard
    # [2026-07-08 14:18:33] 作用：断言资产挂载 API 是阻断条件；理由依据：18191/resourceType/api 必须能转发资产后端。
    assert "$assetMountedProxyReady" in final_guard
    # [2026-07-08 14:18:33] 作用：断言知识库挂载页面是阻断条件；理由依据：别人前端跳转知识库管理使用 18191/knowledgeManagement/。
    assert "$knowledgeMountedWebReady" in final_guard
    # [2026-07-08 14:18:33] 作用：断言知识库挂载 API 仍是阻断条件；理由依据：别人前端跳转后的页面必须通过 18191 转发到 18320。
    assert "$knowledgeMountedProxyReady" in final_guard


# [2026-07-08 14:22:07] 作用：验证全量启动脚本接入 ONEDLP 污染修复和成功态备份；理由依据：用户要求再次遇到加密头乱码时先对照可运行备份恢复，而不是重新安装。
def test_full_stack_launcher_runs_onedlp_repair_and_runtime_backup() -> None:
    # [2026-07-08 14:22:07] 作用：读取启动脚本文本；理由依据：修复和备份是启动脚本的静态合同，可不启动服务检查。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-07-08 14:22:07] 作用：断言启动前调用 ONEDLP 修复脚本；理由依据：污染依赖必须在 Python 服务启动前处理。
    assert "repair_sql_rag_runtime_onedlp.ps1" in source
    # [2026-07-08 14:22:07] 作用：断言启动成功后调用运行时备份脚本；理由依据：成功状态要自动固化为下一次恢复依据。
    assert "backup_sql_rag_runtime.ps1" in source
    # [2026-07-08 14:22:07] 作用：定位启动前修复脚本出现位置；理由依据：修复必须早于主业务脑 Python 启动。
    repair_index = source.find("repair_sql_rag_runtime_onedlp.ps1")
    # [2026-07-08 14:22:07] 作用：定位主业务脑后端启动命令出现位置；理由依据：比较执行顺序需要稳定锚点。
    backend_start_index = source.find("business-brain-service")
    # [2026-07-08 14:22:07] 作用：断言修复脚本位于主业务脑启动之前；理由依据：否则污染 .venv 仍会在 import 阶段失败。
    assert 0 <= repair_index < backend_start_index
    # [2026-07-08 14:35:04] 作用：定位运行时备份脚本真实调用位置；理由依据：顶部变量定义不是执行动作，不能用文件名第一次出现位置判断顺序。
    backup_index = source.rfind("-File $RuntimeBackupScript")
    # [2026-07-08 14:22:07] 作用：定位最终全量 ready 保护语句；理由依据：比较备份和验收条件的执行顺序。
    final_guard_index = source.rfind("全量服务没有全部 ready")
    # [2026-07-08 14:22:07] 作用：断言备份脚本位于最终失败保护之后；理由依据：不能把失败状态保存成可运行基线。
    assert final_guard_index < backup_index
    # [2026-07-08 14:36:58] 作用：断言启动前修复失败会显式阻断主脚本；理由依据：powershell.exe 是 native 命令，失败不会自动抛异常。
    assert "ONEDLP 修复脚本执行失败" in source
    # [2026-07-08 14:36:58] 作用：断言启动后备份失败会显式阻断主脚本；理由依据：成功基线没保存时不能把启动流程当成完全成功。
    assert "SQL_RAG 运行时备份脚本执行失败" in source
    # [2026-07-15 10:04:45] 作用：断言启动器允许统一修复器逐文件恢复 SQL_RAG 源码；理由依据：只修复根虚拟环境仍会遗漏 Knowledge_management 污染。
    assert "-RestoreSource" in source
    # [2026-07-15 10:04:45] 作用：断言启动器不再复用旧知识库后端；理由依据：旧进程加载的不是本次当前工作区逻辑。
    assert "$ReuseExistingKnowledgeBackend" not in source
    # [2026-07-15 10:04:45] 作用：断言启动器不再复用旧知识库前端；理由依据：端口被旧进程占用时必须失败而不是伪装最新服务。
    assert "$ReuseExistingKnowledgeWeb" not in source
    # [2026-07-15 10:04:45] 作用：断言全量 ready 后再次检查 ONEDLP；理由依据：启动期间再次污染时不能创建成功备份。
    assert "启动后 ONEDLP 完整性检查失败" in source
    # [2026-07-15 10:04:45] 作用：断言备份命令携带全栈成功证明；理由依据：没有健康门禁证明的目录不能推进 LATEST。
    assert "-FullStackReady" in source
    # [2026-07-15 10:04:45] 作用：断言备份元数据接收健康门禁集合；理由依据：以后恢复前需要确认基线来自完整前后端服务。
    assert "-HealthGates" in source
    # [2026-07-15 10:04:45] 作用：定位启动后完整性脚本的最后一次真实调用；理由依据：必须证明复检发生在成功备份之前。
    post_integrity_index = source.rfind("-File $RuntimeIntegrityScript")
    # [2026-07-15 10:04:45] 作用：断言启动后复检先于成功备份；理由依据：污染状态不能被固化为新的最新恢复基线。
    assert final_guard_index < post_integrity_index < backup_index
    # [2026-07-08 14:42:18] 作用：断言端口释放保留 WMI Terminate 兜底；理由依据：旧高权限 Python 进程可能拒绝 taskkill 和 Stop-Process。
    assert "Invoke-CimMethod -InputObject $wmiTarget -MethodName Terminate" in source


# [2026-07-29 16:58:54] 作用：验证固定一键入口在启动耗时服务前修复不可读的可移植数据库种子；理由依据：存在但普通用户不可读的 manifest 会让 WebUI 根本没有机会启动。
def test_full_stack_launcher_repairs_portable_clone_seed_before_services() -> None:
    # [2026-07-29 16:58:54] 作用：读取用户唯一执行的正式启动脚本；理由依据：不能只给临时命令增加恢复逻辑。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-07-29 16:58:54] 作用：定位可移植种子恢复器真实调用；理由依据：变量声明不能证明固定入口会执行权限与哈希门禁。
    repair_index = source.find("-File $PortableCloneSeedRepairScript")
    # [2026-07-29 16:58:54] 作用：定位 Docker Compose 正式拉起数据库的位置；理由依据：恢复应在耗时容器与模型启动前完成。
    docker_index = source.find("Compose @('up','-d'")
    # [2026-07-29 16:58:54] 作用：定位 Knowledge 后端正式启动命令；理由依据：不可读种子不能再导致 WebUI 服务全部缺席。
    knowledge_index = source.find("Knowledge_management\\backend\\knowledge_api\\run_server.py")
    # [2026-07-29 16:58:54] 作用：断言恢复器真实调用存在且早于 Docker；理由依据：避免重现等待十几分钟后才抛 PermissionError。
    assert 0 <= repair_index < docker_index
    # [2026-07-29 16:58:54] 作用：断言恢复器早于 Knowledge 后端；理由依据：一键入口必须先保证数据种子可读再启动实际 WebUI 链路。
    assert repair_index < knowledge_index
    # [2026-07-29 16:58:54] 作用：要求父启动器按恢复器退出码失败关闭；理由依据：哈希或路径越界失败不能被 PowerShell native 调用吞掉。
    assert "可移植克隆种子启动前恢复失败" in source


# [2026-07-17 13:56:30] 作用：验证唯一全量入口固定拉起本轮已验收的主业务脑端口且所有桌面子进程隐藏；理由依据：用户只应执行一个 PS1，不再分散多个 PowerShell 或 Docker Desktop 窗口。
def test_full_stack_launcher_uses_current_business_ports_and_hidden_processes() -> None:
    # [2026-07-17 13:56:30] 作用：读取正式一键启动脚本；理由依据：测试必须约束用户实际复制执行的唯一入口。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-07-30 11:38:02] 作用：锁定主后端使用统一部署端口合同；理由依据：local profile 保持 18182，aliyun profile 可切换且不修改共享启动逻辑。
    assert "$BackendPort=Get-ServiceProfilePort 'business_backend'" in source
    # [2026-07-30 11:38:03] 作用：锁定主 WebUI 使用统一部署端口合同；理由依据：local profile 保持 18183，避免测试继续要求已移除的散落常量。
    assert "$WebPort=Get-ServiceProfilePort 'business_web'" in source
    # [2026-08-03 13:39:47] 作用：要求共享引擎对第二套强制Docker Desktop 4.84最低版本；理由依据：目标机4.83已实机复现内部Engine _ping HTTP500。
    assert "if($dockerDesktopVersion-lt[version]'4.84.0')" in source
    # [2026-08-03 13:39:48] 作用：禁止共享引擎在Docker初始化中途关闭全部WSL；理由依据：V9冷恢复打断后端且无法修复内部HTTP500。
    assert "wsl.exe --shutdown" not in source
    # [2026-08-03 15:14:53] 作用：要求第二套Docker首轮Engine判定固定为120秒；理由依据：现场42轮超时证明15分钟等待只会延迟根因诊断。
    assert "Wait-DockerEngineReady -TimeoutSeconds 120" in source
    # [2026-08-03 17:15:15] 作用：要求失败诊断区分内部Engine就绪后的Windows API proxy HTTP500；理由依据：V12两轮目标机日志已提供四项同时命中证据。
    assert "windows_api_proxy_http_500_after_internal_engine_ready" in source
    # [2026-08-03 18:05:23] 作用：要求诊断优先区分第二套直连Engine管道缺失或无响应；理由依据：实际DOCKER_HOST证据必须优先于Desktop UI日志分类。
    assert "direct_linux_engine_pipe_missing_or_unresponsive" in source
    # [2026-08-03 18:05:24] 作用：要求第二套共享引擎固定进程级直连端点；理由依据：全部docker info与Compose调用都必须继承同一DOCKER_HOST。
    assert "$env:DOCKER_HOST=$DockerEngineEndpoint" in source
    # [2026-08-03 18:46:05] 作用：要求共享引擎在Compose前实测并注入Docker VM宿主路径；理由依据：目标机invalid volume specification不能再延迟到init-db阶段才发现。
    assert "Resolve-DockerDesktopDirectInitBindSource" in source
    # [2026-08-03 18:46:06] 作用：要求首选Docker Desktop Linux VM实际挂载根；理由依据：本机直连Engine容器已验证该路径可读。
    assert "/run/desktop/mnt/host/" in source
    # [2026-08-03 18:46:07] 作用：要求选中路径仅在当前启动进程注入；理由依据：不得改动第一套默认Compose路径或用户全局配置。
    assert "$env:SQL_RAG_INIT_BIND_SOURCE=$selectedPath" in source
    # [2026-08-03 18:46:08] 作用：要求路径探针同时验证两个init脚本可读；理由依据：目录存在不足以证明数据库初始化资产完整。
    assert "test -r /sql-rag-init-probe/init-db.sh -a -r /sql-rag-init-probe/init-external-db.sh" in source
    # [2026-08-03 18:49:31] 作用：要求init探针禁止自动拉取镜像；理由依据：缺少离线镜像应立即显示资产缺口而不能长时网络等待。
    assert "docker.exe run --pull never" in source
    # [2026-08-03 18:46:09] 作用：读取Compose文本用于路径合同检查；理由依据：启动器注入变量必须有两个init服务消费。
    compose_source = COMPOSE.read_text(encoding="utf-8-sig")
    # [2026-08-03 18:46:10] 作用：断言参数化init bind合同恰好出现两次；理由依据：内外两库初始化必须同时修复且不可误改其他卷。
    assert compose_source.count("${SQL_RAG_INIT_BIND_SOURCE:-./init}:/init:ro") == 2
    # [2026-08-03 18:05:25] 作用：禁止共享引擎重新修改全局desktop-linux context；理由依据：该行为既耦合第一套又会把第二套重新送进故障Desktop代理。
    assert "@('context','use','desktop-linux')" not in source
    # [2026-08-03 17:15:16] 作用：要求管理员入口通过Explorer ShellExecute启动Desktop；理由依据：不能从管理员PowerShell直接继承完整令牌。
    assert "Start-DockerDesktopForInteractiveUser" in source and ".ShellExecute(" in source
    # [2026-08-03 17:15:17] 作用：要求使用Docker 4.84官方gather而非废弃check；理由依据：V12诊断JSON只得到弃用提示，无法交付产品诊断包。
    assert "@('gather',$officialBundlePath)" in source and "@('check')" not in source
    # [2026-08-03 15:14:55] 作用：要求所有Docker和WSL诊断共用硬超时执行器；理由依据：V11在总等待结束后又被直接诊断命令无限阻塞。
    assert "function Invoke-BoundedDiagnosticCommand" in source
    # [2026-08-03 15:14:56] 作用：禁止恢复直接执行docker desktop status；理由依据：任何诊断子命令都必须有独立超时。
    assert "@(& $DockerCli desktop status" not in source
    # [2026-08-03 15:14:57] 作用：要求同开机周期唯一恢复状态落盘；理由依据：重跑固定入口不得循环restart。
    assert "docker-host-recovery-state.json" in source
    # [2026-08-03 15:14:58] 作用：要求最终失败明确下一步与零破坏操作；理由依据：端口不得部分启动且数据卷不得被重置。
    assert "next_action=restart_windows_once_then_rerun_same_entrypoint" in source and "data_destructive_actions=0" in source
    # [2026-07-17 13:56:30] 作用：要求 Pydantic 完整禁用损坏插件扫描；理由依据：值 1 不能表达官方全禁用语义，最新版服务统一使用 __all__。
    assert "$env:PYDANTIC_DISABLE_PLUGINS='__all__'" in source


# [2026-08-03 09:06:59] 作用：验证 Docker 就绪门禁发生在两个模型启动之前；理由依据：容器引擎失败时不能再留下28001/28002半套进程污染下次重跑。
def test_full_stack_launcher_recovers_docker_before_starting_models() -> None:
    # [2026-08-03 09:07:00] 作用：读取正式共享启动引擎；理由依据：执行顺序必须由用户真实入口源码锁定。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-03 09:07:01] 作用：定位运行阶段 Docker 自恢复调用；理由依据：函数定义本身不代表它在模型之前执行。
    docker_stage = source.index("# [2026-08-03 09:06:45]")
    # [2026-08-03 09:07:02] 作用：定位 Embedding 模型启动分支；理由依据：这是当前两项模型服务的第一个运行副作用。
    model_stage = source.index("if($RestartModel -or !(Test-Embedding)")
    # [2026-08-03 09:07:03] 作用：断言 Docker 阶段严格早于模型阶段；理由依据：冷启动失败必须在任何本地模型进程创建前结束。
    assert docker_stage < model_stage


# [2026-08-03 09:07:04] 作用：验证在线权威克隆具备父进程硬超时与基线回退；理由依据：数据库建连或事务卡住不能再次阻塞全部WebUI端口。
def test_full_stack_launcher_bounds_online_clone_and_preserves_baseline_fallback() -> None:
    # [2026-08-03 09:07:05] 作用：读取正式共享启动引擎；理由依据：回归测试必须覆盖用户固定一键命令实际调用的代码。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-03 09:07:06] 作用：断言在线克隆通过独立进程等待硬上限；理由依据：只给 psycopg 建连超时仍无法限制锁等待和全表复制。
    assert "$onlineCloneProcess.WaitForExit($TimeoutSeconds*1000)" in source
    # [2026-08-03 09:07:07] 作用：断言超时后仍调用已恢复基线验证；理由依据：部署机离线时必须继续使用哈希和数量均通过的本地数据库。
    assert "if(!$WktOnlineCloneReady)" in source


# [2026-07-17 13:56:30] 作用：验证一键入口同时托管本地 Embedding 与已验收 Qwen 运行合同；理由依据：只拉前后端而遗漏 18001，或复用参数漂移的 18002，都不属于全量最新服务。
def test_full_stack_launcher_manages_local_models_and_health_gates() -> None:
    # [2026-07-17 13:56:30] 作用：读取启动器全文；理由依据：模型路径、进程合同与最终 ready 门禁必须在同一入口内闭环。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-07-30 11:38:04] 作用：要求 Embedding 使用统一部署端口合同；理由依据：local profile 仍为 18001，同时允许阿里云 profile 使用独立端口而不串服务。
    assert "$EmbeddingPort=Get-ServiceProfilePort 'embedding_model'" in source
    # [2026-07-17 13:56:30] 作用：要求使用仓库内 Qwen3 Embedding 模型；理由依据：不能把远程 API 或另一模型冒充全本地链路。
    assert "Qwen3-Embedding-0.6B-Q8_0.gguf" in source
    # [2026-07-17 13:56:30] 作用：要求 Embedding 服务进入专用推理模式；理由依据：普通聊天模式不能保证 `/v1/embeddings` 合同。
    assert "--embedding --pooling last" in source
    # [2026-07-17 13:56:30] 作用：要求健康检查覆盖 Embedding；理由依据：仅端口监听不能证明 OpenAI-compatible 模型端点可用。
    assert "function Test-Embedding" in source
    # [2026-07-17 13:56:30] 作用：要求比对 Embedding 进程启动参数；理由依据：健康但模型或端口参数漂移的旧进程不能复用。
    assert "function Test-EmbeddingRuntimeContract" in source
    # [2026-07-17 13:56:30] 作用：要求比对 Qwen 进程启动参数；理由依据：旧 18002 即使返回 models，也可能不是五线程、单 slot、160 token 的最新配置。
    assert "function Test-QwenRuntimeContract" in source
    # [2026-07-17 13:56:30] 作用：要求最终成功条件包含 Embedding；理由依据：18001 不可用时不能报告全栈 ready 或创建成功备份。
    final_guard = source[source.rfind("if(!("):]
    # [2026-07-17 14:08:33] 作用：断言 Embedding 进入最终保护谓词；理由依据：逐行审计要求每条真实断言都有独立紧邻说明。
    assert "$embeddingReady" in final_guard
    # [2026-07-17 13:56:30] 作用：要求最终成功条件同时包含 Qwen；理由依据：前后端 ready 不能掩盖 18002 在启动后退出的情况。
    assert "$qwenReady" in final_guard
    # [2026-07-17 13:56:30] 作用：要求成功备份记录本地 Embedding 门禁；理由依据：LATEST 基线必须证明两个本地模型都真实可用。
    assert "'local_embedding_model'" in source
    # [2026-07-17 13:56:30] 作用：要求成功备份记录本地 Qwen 门禁；理由依据：恢复基线必须证明规划与回答模型真实可用。
    assert "'local_qwen_model'" in source


# [2026-07-30 16:28:00] 作用：验证独立迁移源 PostgreSQL 会随本地/服务器 profile 对齐宿主端口；理由依据：该容器不属于主 Compose，曾在服务器第二套启动后仍占用本地 5432。
def test_full_stack_launcher_reconciles_migrated_postgres_profile_port() -> None:
    # [2026-07-30 16:28:01] 作用：读取用户实际执行的共享一键启动引擎；理由依据：端口修复必须落在固定入口而非临时命令。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-07-30 16:28:02] 作用：断言迁移源端口来自统一 profile；理由依据：本地要求 5432，服务器第二套要求 15432。
    assert "SQL_RAG_MIGRATED_PG_PORT=$MigratedPostgresPort" in source
    # [2026-07-30 16:28:03] 作用：断言一键入口调用迁移源 profile 对齐器；理由依据：仅设置环境变量不会自动重建独立 Compose 容器。
    assert "Ensure-OptionalMigratedPostgresProfile" in source
    # [2026-07-30 16:28:04] 作用：断言运行态读取 HostPort；理由依据：只验证 HostIp=127.0.0.1 无法发现第二套端口串回本地 5432。
    assert "$hostPort=[int]$binding.HostPort" in source
    # [2026-07-30 16:28:05] 作用：断言实际端口必须等于当前 profile；理由依据：portproxy 自身可接受 TCP，不能把代理监听误当成 PostgreSQL 协议就绪。
    assert "$hostPort -ne [int]$MigratedPostgresPort" in source


# [2026-07-30 16:48:07] 作用：验证 Getsoft 数据库跟随统一部署 profile 而不再固定旧开发机地址；理由依据：新服务器应连接本机恢复容器 127.0.0.1:15432。
def test_getsoft_adapter_uses_profile_selected_postgres_host_and_port() -> None:
    # [2026-07-30 16:48:08] 作用：读取正式 Getsoft 适配器源码；理由依据：不能只修改文档或临时进程环境。
    source = GETSOFT_ADAPTER.read_text(encoding="utf-8-sig")
    # [2026-07-30 16:48:09] 作用：断言数据库主机来自共享一键入口；理由依据：本地第一套和服务器第二套只通过 profile 区分。
    assert "$env:SQL_RAG_EXTERNAL_PG_HOST" in source
    # [2026-07-30 16:48:10] 作用：断言数据库宿主端口来自共享 profile；理由依据：服务器宿主端口 15432 不能误用容器内部 5432。
    assert "$env:SQL_RAG_MIGRATED_PG_PORT" in source
    # [2026-07-30 16:48:11] 作用：断言结构化 URI 同时写入目标端口；理由依据：只替换主机仍会连接错误端口。
    assert "$PinnedDatabaseUriBuilder.Port=$PinnedDatabasePort" in source
    # [2026-07-30 16:48:12] 作用：断言回环地址被视为安全数据目标；理由依据：目标服务器数据容器只允许 127.0.0.1 原生监听。
    assert "[System.Net.IPAddress]::IsLoopback" in source


# [2026-07-31 10:46:02] 作用：验证一键启动会修复恢复库与 Getsoft ORM 的结构差异；理由依据：只修改正在运行的数据库不能保护重启和新服务器恢复。
def test_full_stack_launcher_migrates_getsoft_session_company_name_schema() -> None:
    # [2026-07-31 10:46:03] 作用：读取正式共享启动引擎；理由依据：本地和服务器入口最终都调用同一文件。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-07-31 10:46:04] 作用：断言启动器按当前 profile 容器执行兼容迁移；理由依据：两套数据库不能固定只修第一套。
    assert "$profileContainerEnvironment.SQL_RAG_MIGRATED_PG_CONTAINER" in source
    # [2026-07-31 10:46:05] 作用：断言幂等补列语句被固化；理由依据：旧数据库备份缺列时需要自动兼容，新备份重复启动不能报错。
    assert 'ADD COLUMN IF NOT EXISTS gs_name varchar(64)' in source
    # [2026-07-31 10:46:06] 作用：断言历史行会补充稳定非空值；理由依据：只加 NOT NULL 列会因现有会话数据失败。
    assert "COALESCE(NULLIF(btrim(gs_id),''),'unknown')" in source
    # [2026-07-31 10:46:07] 作用：断言迁移门禁在正式执行链中被调用；理由依据：存在函数定义不等于一键部署会运行它。
    assert "Ensure-MigratedPostgresGetsoftSchemaCompatibility" in source


# [2026-07-31 10:46:08] 作用：验证两套 profile 都明确允许同一个企业门户调用知识业务端口；理由依据：本地 18320 和服务器 28320 都会被门户页面直连。
def test_port_profiles_include_exact_knowledge_portal_origins() -> None:
    # [2026-07-31 10:46:09] 作用：读取唯一 profile 配置；理由依据：测试不能维护第二份域名列表。
    profiles = json.loads(PORT_PROFILES.read_text(encoding="utf-8-sig"))["profiles"]
    # [2026-07-31 10:46:10] 作用：逐套验证门户白名单；理由依据：只修 local 会让新服务器部署后重现相同浏览器故障。
    for profile_name in ("local", "aliyun"):
        # [2026-07-31 10:46:11] 作用：取出当前 profile 的精确来源集合；理由依据：允许次序变化但不允许缺少 HTTP/HTTPS 实际入口。
        origins = set(profiles[profile_name]["portal_web_origins"])
        # [2026-07-31 10:46:12] 作用：断言 HTTP 门户来源存在；理由依据：当前用户截图实际通过该来源访问。
        assert "http://mofang.bao1998.com" in origins
        # [2026-07-31 10:46:13] 作用：断言 HTTPS 升级后的同域来源存在；理由依据：浏览器 Origin 包含协议，证书切换后不能再次中断上传。
        assert "https://mofang.bao1998.com" in origins


# [2026-08-06 11:08:00] 作用：验证两套配置分别生成唯一前端挂载身份；理由依据：第二套直连有数据但门户页面为0已证明端口profile不包含挂载合同仍会串线。
def test_frontend_mount_profiles_are_atomic_and_cross_host_isolated() -> None:
    # [2026-08-06 11:08:00] 作用：读取第一套兼容profile和第二套独立profile；理由依据：测试必须同时证明第一套不变与第二套不回落。
    legacy_profiles = json.loads(PORT_PROFILES.read_text(encoding="utf-8-sig"))["profiles"]
    # [2026-08-06 11:08:00] 作用：读取第二套独立单profile合同；理由依据：目标服务器正式入口不会消费legacy aliyun对象。
    server_profile = json.loads(SERVER_PROFILE.read_text(encoding="utf-8-sig"))
    # [2026-08-06 11:08:00] 作用：建立正式第一套和第二套测试集合；理由依据：兼容aliyun只用于端口碰撞，不可替代服务器独立合同。
    profiles = {"local": legacy_profiles["local"], "server_second_ports": server_profile}
    # [2026-08-06 11:08:00] 作用：声明两套期望公开根；理由依据：主机和端口必须整体切换而非仅修改其中一项。
    expected_bases = {"local": "http://172.18.1.212:18191", "server_second_ports": "http://172.18.1.233:28191"}
    # [2026-08-06 11:08:00] 作用：逐套校验挂载配置和派生URL；理由依据：任一套缺字段都会重新启用WebUI默认值。
    for profile_name, profile in profiles.items():
        # [2026-08-06 11:08:00] 作用：读取当前profile前端合同；理由依据：端口表本身不能表达两个业务挂载路径。
        mounts = profile["frontend_mounts"]
        # [2026-08-06 11:08:00] 作用：断言统一网关协议和服务归属；理由依据：现有生产网关由asset_web以HTTP同时承载两项页面。
        assert (mounts["scheme"], mounts["gateway_service"]) == ("http", "asset_web")
        # [2026-08-06 11:08:00] 作用：断言两项正式路径；理由依据：别人前端挂载合同不得由脚本散落字符串维护。
        assert (mounts["asset_path"], mounts["knowledge_path"]) == ("/resourceType/", "/knowledgeManagement/")
        # [2026-08-06 11:08:00] 作用：按当前profile字段生成公开根；理由依据：测试复现启动器的单一事实源算法。
        public_base = f'{mounts["scheme"]}://{profile["lan_ip"]}:{profile["ports"][mounts["gateway_service"]]}'
        # [2026-08-06 11:08:00] 作用：断言第一套与第二套公开根精确值；理由依据：不允许212主机配28191端口或233主机配18191端口。
        assert public_base == expected_bases[profile_name]
    # [2026-08-06 11:08:00] 作用：断言两套正式公开根互不相同；理由依据：相同入口会重新形成服务共生。
    assert len(set(expected_bases.values())) == 2


# [2026-08-06 11:08:00] 作用：验证共享启动器注入并硬验收前端profile身份；理由依据：JSON配置正确但进程未消费仍会重现截图故障。
def test_full_stack_launcher_requires_frontend_runtime_profile_identity() -> None:
    # [2026-08-06 11:08:00] 作用：读取正式共享启动引擎；理由依据：两套固定入口最终都由该文件启动自己的WebUI。
    source = LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-06 11:08:00] 作用：声明从配置解析、进程注入、运行态探针到最终门禁的关键合同；理由依据：只实现其中一段不能长期阻断串线。
    required = (
        "$FrontendMountProfile=$ServicePortProfile.frontend_mounts",
        "$FrontendPublicBaseUrl=\"$FrontendScheme`://$FrontendProfileHost`:$FrontendGatewayPort\"",
        "'--deployment-profile',$DeploymentProfile,'--public-base-url',$FrontendPublicBaseUrl",
        'Invoke-RestMethod "$AssetTypeWebUrl/runtime-profile.json"',
        "frontend_profile_isolation=$frontendProfileReady",
    )
    # [2026-08-06 11:08:00] 作用：逐项断言完整前端profile链存在；理由依据：测试失败信息需直接指出漏掉的阶段。
    for marker in required:
        # [2026-08-06 11:08:00] 作用：断言当前关键合同文本；理由依据：防止后续重构静默删除profile门禁。
        assert marker in source, marker


# [2026-08-31 18:21:57] 作用：验证回环恢复库经本 profile 容器私网接入 PgBouncer；理由依据：目标机已实证 host.docker.internal 到 25434 无路由而容器 DNS 的 5432 可执行 SELECT 1。
def test_commercial_pgbouncer_uses_profile_migrated_postgres_private_network() -> None:
    # [2026-08-31 18:21:57] 作用：读取第一套与第二套共用的商业启动器；理由依据：临时容器配置成功不能替代固定一键入口的永久实现。
    source = COMMERCIAL_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-31 18:21:57] 作用：截取 PgBouncer 上游解析到 Compose 环境注入之间的路由合同；理由依据：测试应排除后续无关的商业服务文本。
    routing = source[source.index("$pgbouncerUsesProfileMigratedPostgres="):source.index("$composeEnvironment=")]
    # [2026-08-31 18:21:57] 作用：要求只把回环数据库识别为本 profile 迁移容器；理由依据：外部 PostgreSQL 主机必须继续沿用既有直连行为。
    assert "$pgbouncerUsesProfileMigratedPostgres=($knowledgeDatabaseUri.Host-in@('127.0.0.1','localhost'))" in routing
    # [2026-08-31 18:21:57] 作用：要求数据库容器名按当前前缀派生；理由依据：第一套和第二套不得引用彼此容器。
    assert '$migratedPostgresContainer="$ContainerNamePrefix-migrated-source-postgres"' in routing
    # [2026-08-31 18:21:57] 作用：要求迁移网络来自共享引擎注入的当前 profile Compose 项目；理由依据：不得猜测或写死第一套网络。
    assert "$migratedPostgresProject=([string]$env:SQL_RAG_MIGRATED_PG_PROJECT).Trim()" in routing
    # [2026-08-31 18:21:57] 作用：要求回环恢复库使用容器 DNS 和内部 PostgreSQL 端口；理由依据：宿主发布端口 5432/25434 不属于容器私网路由。
    assert "$pgbouncerUpstreamHost=if($pgbouncerUsesProfileMigratedPostgres){$migratedPostgresContainer}else{$knowledgeDatabaseUri.Host}" in routing
    # [2026-08-31 18:21:57] 作用：要求外部数据库端口保留原 URL 值；理由依据：第一套已跑通的非回环 PostgreSQL 不得被强制改为容器 5432。
    assert "$pgbouncerUpstreamPort=if($pgbouncerUsesProfileMigratedPostgres){5432}else{$knowledgeDatabaseUri.Port}" in routing
    # [2026-08-31 18:21:57] 作用：禁止恢复旧的 Windows Host Gateway 上游分支；理由依据：该分支正是目标机 No route to host 的确定根因。
    assert "$pgbouncerUpstreamHost=if($knowledgeDatabaseUri.Host-in@('127.0.0.1','localhost')){'host.docker.internal'}else{$knowledgeDatabaseUri.Host}" not in source


# [2026-08-31 18:21:57] 作用：验证 PgBouncer 在完整商业服务图之前完成接线和真实查询门禁；理由依据：35/36 泛化错误必须被提前为具名数据库路由故障。
def test_commercial_pgbouncer_private_route_precedes_full_compose_start() -> None:
    # [2026-08-31 18:21:57] 作用：读取正式商业启动器；理由依据：执行顺序必须由一键入口源码而不是现场手工命令锁定。
    source = COMMERCIAL_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-08-31 18:21:57] 作用：定位只创建 PgBouncer 的阶段；理由依据：网络接线前容器必须存在但不能提前等待错误健康探针。
    create_stage = source.index("create --no-build --pull never km-pgbouncer")
    # [2026-08-31 18:21:57] 作用：定位 profile 私网接线阶段；理由依据：仅 PgBouncer 应加入迁移数据库项目网络。
    network_stage = source.index("docker network connect $migratedPostgresNetwork $pgbouncerContainer")
    # [2026-08-31 18:21:57] 作用：定位 PgBouncer 单服务启动阶段；理由依据：配置生成必须消费完成接线后的正确环境。
    start_stage = source.index("start km-pgbouncer")
    # [2026-08-31 18:21:57] 作用：定位独立预检成功阶段；理由依据：真实 SQL 健康必须先于其他三十五个服务。
    preflight_stage = source.index("KNOWLEDGE_COMMERCIAL_PGBOUNCER_PREFLIGHT_READY")
    # [2026-08-31 18:21:57] 作用：定位完整商业 Compose 启动阶段；理由依据：依赖图只能在连接池健康后展开。
    full_start_stage = source.index("up -d --no-build --pull never --remove-orphans")
    # [2026-08-31 18:21:57] 作用：断言创建、接线、启动、预检和全量启动严格有序；理由依据：任一步乱序都会重现 unhealthy 依赖阻断。
    assert create_stage < network_stage < start_stage < preflight_stage < full_start_stage
    # [2026-08-31 18:21:57] 作用：要求接线对象是 PgBouncer 而不是迁移 PostgreSQL；理由依据：数据库不能暴露给全部商业服务所在网络。
    assert "docker network connect $commercialNetwork $migratedPostgresContainer" not in source
    # [2026-08-31 18:21:57] 作用：读取第二套独立 profile；理由依据：无 VPN 但有互联网必须显式走与第一套一致的源码构建分支。
    server_profile = json.loads(SERVER_PROFILE.read_text(encoding="utf-8-sig"))
    # [2026-08-31 18:21:57] 作用：断言第二套默认 source_build；理由依据：profile 身份不得再次静默选择离线导入旧镜像。
    assert server_profile["commercial_runtime_mode"] == "source_build"


# [2026-09-01 17:23:10] 作用：验证第二套商业网段固定且第一套基础网络合同保持不变；理由依据：目标 172.20.0.0/16 与宿主 172.20.192.1 重叠，但修复不能迁移第一套已跑通的 172.27 网络。
def test_second_commercial_network_is_fixed_without_changing_first_stack_compose() -> None:
    # [2026-09-01 17:23:10] 作用：读取第二套独立 profile；理由依据：固定网段必须是版本化配置而不是现场临时命令。
    server_profile = json.loads(SERVER_PROFILE.read_text(encoding="utf-8-sig"))
    # [2026-09-01 17:23:10] 作用：读取第一套兼容 profile；理由依据：断言它没有接收第二套 Docker 网络字段。
    local_profile = json.loads(PORT_PROFILES.read_text(encoding="utf-8-sig"))["profiles"]["local"]
    # [2026-09-01 17:23:10] 作用：读取商业基础 Compose；理由依据：第一套继续消费原单文件网络声明。
    compose_source = COMMERCIAL_COMPOSE.read_text(encoding="utf-8-sig")
    # [2026-09-01 17:23:10] 作用：断言第二套使用小型且确定的 RFC1918 /24；理由依据：36 个服务容量充足并避开目标当前 172.18、172.20 和 172.23 宿主网段。
    assert server_profile["docker"]["commercial_network"] == {"subnet": "10.253.233.0/24", "gateway": "10.253.233.1"}
    # [2026-09-01 17:23:10] 作用：断言第一套 profile 不含商业固定 IPAM；理由依据：第一套不得进入第二套网络重建分支。
    assert "docker" not in local_profile or "commercial_network" not in local_profile.get("docker", {})
    # [2026-09-01 17:23:10] 作用：断言基础 Compose 仍未写死任一子网；理由依据：第一套已验收的网络创建行为保持逐字语义不变。
    assert "ipam:" not in compose_source and "10.253.233.0/24" not in compose_source


# [2026-09-02 14:41:08] 作用：验证多网络 inspect JSON 在 Windows PowerShell 5.1 中逐项展开；理由依据：1154 把全部网络包成单个 System.Object[] 后错误输出 recreate=False。
def test_commercial_network_inspect_array_is_flattened_under_windows_powershell_51() -> None:
    # [2026-09-02 14:41:08] 作用：读取正式商业启动器；理由依据：实际一键入口必须采用经过 PS5.1 验证的展开表达式。
    source = COMMERCIAL_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-09-02 14:41:08] 作用：锁定网络 JSON 数组的显式逐项展开；理由依据：恢复双层 @() 会让 foreach 只迭代一个 Object[]。
    assert "$dockerNetworkDocuments=@(($dockerNetworkInspectText|ConvertFrom-Json)|ForEach-Object{$_})" in source
    # [2026-09-02 14:41:08] 作用：构造两张网络的最小 PowerShell 5.1 运行夹具；理由依据：第二项模拟目标商业网络并要求可被名称精确选中。
    fixture_script = r"""
$raw='[{"Name":"first-network"},{"Name":"sql-rag-server-km-commercial-internal"}]'
$documents=@(($raw|ConvertFrom-Json)|ForEach-Object{$_})
$target=@($documents|Where-Object{$_.Name-eq'sql-rag-server-km-commercial-internal'})
Write-Output "COUNT=$($documents.Count) TARGET=$($target.Count)"
"""
    # [2026-09-02 14:41:08] 作用：用系统 Windows PowerShell 5.1 执行数组夹具；理由依据：pwsh 7 与目标机的 ConvertFrom-Json 枚举语义不能互相替代。
    completed = subprocess.run(["powershell.exe", "-NoProfile", "-Command", fixture_script], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    # [2026-09-02 14:41:08] 作用：要求两项均展开且商业网络唯一命中；理由依据：这是 recreate 判断能够读取真实 172.20 IPAM 的前提。
    assert completed.returncode == 0 and "COUNT=2 TARGET=1" in completed.stdout, completed.stderr or completed.stdout


# [2026-09-02 15:29:04] 作用：验证端点 Compose 标签通过结构化 JSON 在 Windows PowerShell 5.1 中读取；理由依据：目标机实证 Go-template 内层引号被剥离并报 function com not defined。
def test_commercial_endpoint_project_label_avoids_native_go_template_quoting() -> None:
    # [2026-09-02 15:29:04] 作用：读取正式商业启动器；理由依据：回归必须约束第二套固定入口实际调用的端点所有权门禁。
    source = COMMERCIAL_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-09-02 15:29:04] 作用：截取旧网络重建块；理由依据：只审计发生目标 PS5.1 引号丢失的端点标签读取边界。
    recreate_block = source.split("if($commercialNetworkRequiresRecreate){", 1)[1].split("create --no-build --pull never km-pgbouncer", 1)[0]
    # [2026-09-02 15:29:04] 作用：禁止恢复带内层引号的 Docker Go-template；理由依据：PowerShell 5.1 原生参数层会把标签键双引号剥掉。
    assert "index .Config.Labels" not in recreate_block
    # [2026-09-02 15:29:04] 作用：要求读取完整容器 JSON 并按带点号属性取项目标签；理由依据：结构化解析不依赖 cmdline 双引号保留行为。
    assert all(marker in recreate_block for marker in ("$actualEndpointInspectText", "ConvertFrom-Json", ".Config.Labels", ".'com.docker.compose.project'"))
    # [2026-09-02 15:29:04] 作用：构造带点号 Compose 标签键的 PowerShell 5.1 运行夹具；理由依据：静态文本断言不能替代目标解释器的真实属性解析。
    fixture_script = r"""
$raw='[{"Config":{"Labels":{"com.docker.compose.project":"sql-rag-server-km-commercial"}}}]'
$document=($raw|ConvertFrom-Json)[0]
$labels=$document.Config.Labels
$project=if($null-eq$labels){''}else{[string]$labels.'com.docker.compose.project'}
Write-Output "PROJECT=$project"
"""
    # [2026-09-02 15:29:04] 作用：用系统 Windows PowerShell 5.1 执行结构化标签夹具；理由依据：目标失败只存在于该解释器与原生参数组合。
    completed = subprocess.run(["powershell.exe", "-NoProfile", "-Command", fixture_script], capture_output=True, text=True, encoding="utf-8", errors="replace", check=False)
    # [2026-09-02 15:29:04] 作用：要求结构化标签精确返回第二套商业项目；理由依据：端点删除授权必须获得未丢字符的完整项目名。
    assert completed.returncode == 0 and "PROJECT=sql-rag-server-km-commercial" in completed.stdout, completed.stderr or completed.stdout


# [2026-09-01 17:23:10] 作用：验证固定网段在第二套专属 override 中生效并先做双层冲突检查；理由依据：不能用另一个未经验证的固定网段替换 172.20 冲突。
def test_commercial_launcher_preflights_and_rebuilds_only_owned_second_network() -> None:
    # [2026-09-01 17:23:10] 作用：读取正式商业启动器；理由依据：测试覆盖一键入口实际执行逻辑。
    source = COMMERCIAL_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-09-01 17:23:10] 作用：声明固定网络从读取到展开验收的关键标记；理由依据：缺任一阶段都可能静默回到 Docker 自动分配。
    required = (
        # [2026-09-01 17:23:10] 作用：要求从 profile 读取商业网络；理由依据：第二套 IPAM 的唯一事实源是独立配置。
        "commercial_network",
        # [2026-09-01 17:23:10] 作用：要求检查 Windows 活跃路由；理由依据：本次冲突首先存在于目标宿主 172.20.192.1。
        "Get-NetRoute -AddressFamily IPv4 -State Alive",
        # [2026-09-01 17:23:10] 作用：要求检查全部 Docker 网络；理由依据：新候选也不能覆盖数据库或其他项目私网。
        "docker.exe network inspect @dockerNetworkNames",
        # [2026-09-01 17:23:10] 作用：要求使用无密钥运行时 override；理由依据：基础 Compose 和第一套保持不变。
        "docker-compose.network.override.yml",
        # [2026-09-01 17:23:10] 作用：要求回读展开后的 IPAM；理由依据：文件写入不能冒充 Compose 消费成功。
        "$expandedCommercialIpamConfigs",
        # [2026-09-01 17:23:10] 作用：要求网络修复具备现场证据标记；理由依据：目标日志应直接区分修复前后。
        "KNOWLEDGE_COMMERCIAL_NETWORK_RECREATED",
    )
    # [2026-09-01 17:23:10] 作用：逐项断言固定网络完整链路；理由依据：失败信息直接指出缺失阶段。
    for marker in required:
        # [2026-09-01 17:23:10] 作用：断言当前网络合同文本；理由依据：防止后续重构移除关键门禁。
        assert marker in source, marker
    # [2026-09-01 17:23:10] 作用：定位网络重建与 PgBouncer 创建阶段；理由依据：只在镜像预检完成后缩短第二套停机窗口。
    network_recreate_stage = source.index("if($commercialNetworkRequiresRecreate)")
    # [2026-09-01 17:23:10] 作用：定位 PgBouncer 创建阶段；理由依据：固定 bridge 必须先于任何商业容器重建。
    pgbouncer_create_stage = source.index("create --no-build --pull never km-pgbouncer")
    # [2026-09-01 17:23:10] 作用：断言网络迁移先于商业容器创建；理由依据：旧冲突网络不能被 Compose 继续复用。
    assert network_recreate_stage < pgbouncer_create_stage
    # [2026-09-01 17:23:10] 作用：禁止网络迁移删除命名卷；理由依据：RabbitMQ、Redis、MinIO、Beat、Prometheus 和 Grafana 数据必须保留。
    assert "down -v" not in source and "down --volumes" not in source
    # [2026-09-01 17:23:10] 作用：要求第一套通过无字段条件绕过固定网络；理由依据：本修复只允许影响 server_second_ports。
    assert "$commercialNetworkUsesFixedIpam=($null-ne$commercialNetworkContractProperty)" in source


# [2026-09-01 18:28:28] 作用：验证旧网络活跃端点按精确所有权关闭且迁移 PostgreSQL 只断网不删除；理由依据：目标实机证明 Compose down 可遗漏旧端点并在 PgBouncer create 阶段返回 active endpoints。
def test_commercial_network_recreate_closes_exact_endpoints_without_deleting_volumes() -> None:
    # [2026-09-01 18:28:28] 作用：读取正式商业启动器；理由依据：回归必须覆盖目标实际执行的第二套网络迁移代码。
    source = COMMERCIAL_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-09-01 18:28:28] 作用：截取网络重建到 PgBouncer 创建之间的唯一生命周期块；理由依据：避免其他稳定启动阶段的同名 Docker 命令干扰断言。
    recreate_block = source.split("if($commercialNetworkRequiresRecreate){", 1)[1].split("create --no-build --pull never km-pgbouncer", 1)[0]
    # [2026-09-01 18:28:28] 作用：要求删除名单来自 Compose 展开的精确容器名；理由依据：前缀或项目名不足以覆盖旧网络的真实端点集合。
    assert "$expectedCommercialContainerNames" in recreate_block
    # [2026-09-01 18:28:28] 作用：要求逐端点校验 Compose 项目标签；理由依据：不得停止其他项目的同名或相似前缀容器。
    assert "com.docker.compose.project" in recreate_block and "$actualEndpointProject-ne$expectedEndpointProject" in recreate_block
    # [2026-09-01 18:28:28] 作用：要求商业容器通过精确数组移除；理由依据：目标旧网络上的全部活跃商业端点必须在删网前离开。
    assert "docker.exe rm --force @commercialContainersToRemove" in recreate_block
    # [2026-09-01 18:28:28] 作用：要求迁移 PostgreSQL 仅断开错误商业网络；理由依据：数据库容器、进程、卷和自身私网必须保持运行。
    assert "docker.exe network disconnect --force $commercialNetwork $migratedPostgresContainer" in recreate_block
    # [2026-09-01 18:28:28] 作用：要求删网前回读并阻断任何残余端点；理由依据：Docker 进度文本和退出码不能替代零端点运行事实。
    assert "$remainingCommercialNetworkEndpoints.Count-gt0" in recreate_block
    # [2026-09-01 18:28:28] 作用：禁止重新依赖已在目标机漏端点的 Compose down；理由依据：网络迁移必须按 daemon 当前容器事实闭环。
    assert "@composeCommandArguments down" not in recreate_block and "down --remove-orphans" not in recreate_block
    # [2026-09-01 18:28:28] 作用：禁止任何卷删除参数；理由依据：18 个命名卷中的队列、缓存、对象和监控数据必须保留。
    assert " rm --force --volumes " not in recreate_block and " down -v" not in recreate_block and "down --volumes" not in recreate_block
    # [2026-09-01 18:28:28] 作用：定位商业容器移除、数据库断网、零端点检查和删网步骤；理由依据：操作顺序决定数据库与卷是否安全。
    remove_stage = recreate_block.index("docker.exe rm --force @commercialContainersToRemove")
    # [2026-09-01 18:28:28] 作用：定位迁移 PostgreSQL 错误网络断开步骤；理由依据：它必须发生在商业容器移除后且不能变成容器删除。
    disconnect_stage = recreate_block.index("docker.exe network disconnect --force $commercialNetwork $migratedPostgresContainer")
    # [2026-09-01 18:28:28] 作用：定位零端点硬门禁；理由依据：旧网络只有在 daemon 回读为空后才可删除。
    endpoint_gate_stage = recreate_block.index("$remainingCommercialNetworkEndpoints.Count-gt0")
    # [2026-09-01 18:28:28] 作用：定位旧商业网络删除步骤；理由依据：固定 IPAM 需要重新创建 bridge，但删除必须是最后一步。
    network_remove_stage = recreate_block.index("docker.exe network rm $commercialNetwork")
    # [2026-09-01 18:28:28] 作用：断言安全迁移顺序；理由依据：先清商业端点、再保留数据库断网、再证实为空、最后删网。
    assert remove_stage < disconnect_stage < endpoint_gate_stage < network_remove_stage


# [2026-09-02 14:33:58] 作用：验证固定网段已匹配时仍会在 PgBouncer create 前清理迁移 PostgreSQL 历史 endpoint；理由依据：目标 1154 实证 recreate=False 会跳过旧重建分支并触发 active endpoints。
def test_matching_commercial_network_still_repairs_migrated_postgres_orphan_endpoint() -> None:
    # [2026-09-02 14:33:58] 作用：读取正式商业启动器；理由依据：回归必须锁定第二套固定一键入口的真实执行顺序。
    source = COMMERCIAL_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-09-02 14:33:58] 作用：定位旧网络重建分支；理由依据：新清理路径必须位于该可选分支之后才能覆盖 recreate=False。
    recreate_stage = source.index("if($commercialNetworkRequiresRecreate){")
    # [2026-09-02 14:33:58] 作用：定位网络已匹配时的数据库双向状态判断；理由依据：这是 1154 缺失的独立生命周期检查。
    orphan_repair_stage = source.index("$migratedPostgresReportsCommercialNetwork=($null-ne$migratedPostgresCurrentNetworks.PSObject.Properties[$commercialNetwork])")
    # [2026-09-02 14:33:58] 作用：定位 PgBouncer 创建边界；理由依据：错误数据库 endpoint 必须在 Compose 尝试复用商业网络前消失。
    pgbouncer_create_stage = source.index("create --no-build --pull never km-pgbouncer")
    # [2026-09-02 14:33:58] 作用：断言重建检查、独立错网修复和 PgBouncer 创建严格有序；理由依据：recreate=False 只能跳过重建，不能跳过 endpoint 修复。
    assert recreate_stage < orphan_repair_stage < pgbouncer_create_stage
    # [2026-09-02 14:33:58] 作用：截取独立错网清理块；理由依据：安全断言不得由旧重建分支中的同名命令误满足。
    orphan_repair_block = source.split("# [2026-09-02 14:33:58] 作用：仅对固定 IPAM 且使用本 profile 迁移 PostgreSQL 的部署检查历史错网", 1)[1].split("# [2026-09-02 10:30:25] 作用：声明当前 profile 的 PgBouncer 容器身份", 1)[0]
    # [2026-09-02 14:33:58] 作用：要求新路径仅服务固定 IPAM 与当前 profile 迁移数据库；理由依据：第一套和外部 PostgreSQL 不能进入该修复。
    assert "if($commercialNetworkUsesFixedIpam-and$pgbouncerUsesProfileMigratedPostgres)" in orphan_repair_block
    # [2026-09-02 14:33:58] 作用：要求网络已存在才读取和修改 endpoint；理由依据：首次部署仍应让 Compose 原子创建网络。
    assert "$currentCommercialNetworkNames-contains$commercialNetwork" in orphan_repair_block
    # [2026-09-02 14:33:58] 作用：要求数据库容器侧与商业网络侧双向一致；理由依据：单侧残留状态必须失败关闭而不是强制修改。
    assert "$migratedPostgresReportsCommercialNetwork-ne$commercialNetworkReportsMigratedPostgres" in orphan_repair_block
    # [2026-09-02 14:33:58] 作用：要求断开前后数据库都保持运行且健康；理由依据：部署网络修复不得成为数据库重启或恢复逻辑。
    assert orphan_repair_block.count("running|healthy") == 2
    # [2026-09-02 14:33:58] 作用：要求断开前后均验证 profile 私网；理由依据：PgBouncer 必须继续通过内部 5432 访问原数据库。
    assert orphan_repair_block.count("PSObject.Properties[$migratedPostgresNetwork]") >= 2
    # [2026-09-02 14:33:58] 作用：要求唯一变更是断开错误商业 bridge；理由依据：不得停止、删除数据库或移除任何卷。
    assert "docker.exe network disconnect --force $commercialNetwork $migratedPostgresContainer" in orphan_repair_block
    # [2026-09-02 14:33:58] 作用：禁止独立修复块删除容器、网络或卷；理由依据：当前问题只属于一个错误 endpoint。
    assert "docker.exe rm" not in orphan_repair_block and "docker.exe network rm" not in orphan_repair_block and "--volumes" not in orphan_repair_block
    # [2026-09-02 14:33:58] 作用：要求日志暴露网络匹配但清理历史 endpoint 的专属证据；理由依据：现场不能再把 READY 或 recreate=False 误当成完整服务就绪。
    assert "KNOWLEDGE_COMMERCIAL_MIGRATED_POSTGRES_ORPHAN_ENDPOINT_REPAIRED" in orphan_repair_block


# [2026-09-02 10:31:36] 作用：验证固定 IPAM profile 在 PgBouncer create 前后都闭合商业网络 endpoint；理由依据：目标已复现停止残留容器缺 endpoint 导致 Compose create 提前失败。
def test_commercial_launcher_reconciles_pgbouncer_before_and_after_create() -> None:
    # [2026-09-02 10:31:36] 作用：读取正式商业启动器；理由依据：回归必须锁定一键入口而不是现场手工补线。
    source = COMMERCIAL_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-09-02 10:31:36] 作用：声明唯一 PgBouncer 容器身份文本；理由依据：创建前后所有验真必须命中当前 profile 的同一容器。
    container_declaration = '$pgbouncerContainer="$ContainerNamePrefix-km-pgbouncer"'
    # [2026-09-02 10:31:36] 作用：要求容器身份只声明一次；理由依据：重复声明曾把创建前修复和创建后验收拆成不一致状态。
    assert source.count(container_declaration) == 1
    # [2026-09-02 10:31:36] 作用：定位创建前幂等补接调用；理由依据：停止残留容器必须在 Compose create 之前恢复 endpoint。
    preflight_stage = source.index("Ensure-KmPgbouncerCommercialNetwork -ContainerName $pgbouncerContainer -NetworkName $commercialNetwork -ExpectedProject $commercialProject -RequireNetwork $false")
    # [2026-09-02 10:31:36] 作用：定位 PgBouncer Compose 创建调用；理由依据：回归必须证明补接先于已复现失败边界。
    create_stage = source.index("create --no-build --pull never km-pgbouncer")
    # [2026-09-02 10:31:36] 作用：定位创建后硬门禁调用；理由依据：create 返回零退出码仍不能替代网络/容器双向事实。
    post_create_stage = source.index("Ensure-KmPgbouncerCommercialNetwork -ContainerName $pgbouncerContainer -NetworkName $commercialNetwork -ExpectedProject $commercialProject -RequireNetwork $true")
    # [2026-09-02 11:21:53] 作用：定位容器启动后的运行态网络门禁；理由依据：停止态 create 成功不能证明重启后 active endpoint 已恢复。
    runtime_stage = source.index("KNOWLEDGE_COMMERCIAL_PGBOUNCER_NETWORK_RUNTIME_READY")
    # [2026-09-02 11:21:53] 作用：定位 PgBouncer start 调用；理由依据：运行态门禁必须紧随真正启动之后执行。
    start_stage = source.index("start km-pgbouncer")
    # [2026-09-02 10:31:36] 作用：断言创建前补接、Compose create、创建后验收严格有序；理由依据：任何乱序都会把网络错误重新改写成健康超时。
    assert preflight_stage < create_stage < post_create_stage
    # [2026-09-02 11:21:53] 作用：断言 start 后立即验证 active endpoint；理由依据：关机重启路径必须在进入完整服务图前获得明确网络证据。
    assert start_stage < runtime_stage
    # [2026-09-02 10:31:36] 作用：要求两个调用都受固定 IPAM 条件保护；理由依据：第一套没有固定网络字段，不能进入第二套 endpoint 生命周期。
    assert source.count("if($commercialNetworkUsesFixedIpam){") >= 3
    # [2026-09-02 10:31:36] 作用：要求创建前调用允许首次缺失网络而不手工制造旁路；理由依据：首次部署仍必须由 Compose 原子创建网络和容器。
    assert "-RequireNetwork $false" in source
    # [2026-09-02 10:31:36] 作用：要求创建后调用把缺失网络升级为硬失败；理由依据：固定商业网络未落盘时不得启动连接池。
    assert "-RequireNetwork $true" in source
    # [2026-09-02 10:31:36] 作用：要求日志暴露创建前后两个可审计标记；理由依据：目标机现场需要区分首次、复用和残留补接结果。
    assert "KNOWLEDGE_COMMERCIAL_PGBOUNCER_NETWORK_PREFLIGHT_READY" in source
    # [2026-09-02 10:31:36] 作用：要求日志暴露创建后双向闭环标记；理由依据：后续 PostgreSQL 私网接线必须建立在真实 DNS endpoint 上。
    assert "KNOWLEDGE_COMMERCIAL_PGBOUNCER_NETWORK_READY" in source
    # [2026-09-02 11:21:53] 作用：要求运行态门禁检查 active endpoint；理由依据：ready 日志不能只由容器启动退出码构成。
    assert "ActiveEndpoint" in source and "运行态缺少 active endpoint" in source


# [2026-09-02 10:31:36] 作用：验证 PgBouncer helper 只修复归属正确的停止容器网络且不删除业务资源；理由依据：第二套网络修复不能扩大为第一套或命名卷生命周期变更。
def test_pgbouncer_network_helper_is_fail_closed_and_volume_safe() -> None:
    # [2026-09-02 10:31:36] 作用：读取正式商业启动器；理由依据：helper 是部署层唯一允许修改 endpoint 的代码边界。
    source = COMMERCIAL_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-09-02 10:31:36] 作用：截取 helper 实现；理由依据：静态断言不能被同名业务文本误满足。
    helper = source.split("function Ensure-KmPgbouncerCommercialNetwork", 1)[1].split("# [2026-08-29 18:32:00]", 1)[0]
    # [2026-09-02 10:31:36] 作用：要求校验容器 Compose 项目和服务标签；理由依据：名称相同不足以证明当前 profile 所有权。
    assert "com.docker.compose.project" in helper and "com.docker.compose.service" in helper
    # [2026-09-02 10:31:36] 作用：要求运行中网络不一致时拒绝隐式抖动；理由依据：一键启动不能无提示断开正在服务的连接池。
    assert "运行中网络状态不一致，拒绝隐式断网" in helper
    # [2026-09-02 10:31:36] 作用：要求停止残留容器使用带服务别名的网络补接；理由依据：Compose 和 Worker 通过 km-pgbouncer DNS 名解析连接池。
    assert "docker.exe network connect --alias km-pgbouncer $NetworkName $ContainerName" in helper
    # [2026-09-02 10:31:36] 作用：要求接线后同时回读网络与容器；理由依据：单侧 JSON 残留不能证明 Docker endpoint 已真实存在。
    assert "verifyNetworkDocument" in helper and "verifyContainerDocument" in helper
    # [2026-09-02 10:31:36] 作用：禁止 helper 删除容器或卷；理由依据：修复只允许改变 PgBouncer endpoint，不得损坏持久化队列、缓存和对象数据。
    assert "docker.exe rm" not in helper and "down" not in helper and "--volumes" not in helper


# [2026-09-02 11:20:30] 作用：验证网络重建后的停止容器能识别陈旧 ID 并保留别名；理由依据：Windows/Docker 重启后同名新 bridge 可能让下一次 start 才暴露网络不存在。
def test_pgbouncer_network_helper_reconciles_recreated_network_id() -> None:
    # [2026-09-02 11:20:30] 作用：读取正式商业启动器；理由依据：回归必须锁定实际部署 helper 而不是临时夹具实现。
    source = COMMERCIAL_LAUNCHER.read_text(encoding="utf-8-sig")
    # [2026-09-02 11:20:30] 作用：截取 helper 实现；理由依据：断言只覆盖网络状态修复边界。
    helper = source.split("function Ensure-KmPgbouncerCommercialNetwork", 1)[1].split("# [2026-08-29 18:32:00]", 1)[0]
    # [2026-09-02 11:20:30] 作用：要求读取容器和当前网络的 NetworkID；理由依据：同名网络不足以证明停止容器仍指向有效 bridge。
    assert "$containerNetworkId" in helper and "$currentNetworkId" in helper and "NetworkID" in helper
    # [2026-09-02 11:20:30] 作用：要求陈旧 ID 和停止态异常 endpoint 进入重接判定；理由依据：两种状态都会在真正 start 阶段造成红色超时。
    assert "$networkIdMismatch" in helper and "$stoppedEndpointMismatch" in helper
    # [2026-09-02 11:20:30] 作用：要求重接前保存原别名；理由依据：修复网络不能改变 Compose 容器名和服务 DNS 合同。
    assert "$reconnectAliases" in helper and "$networkConnectArguments" in helper
    # [2026-09-02 11:20:30] 作用：要求保留单别名的稳定调用；理由依据：既有 PowerShell 5.1 路径仍需可审计且避免无谓参数重排。
    assert "docker.exe network connect --alias km-pgbouncer $NetworkName $ContainerName" in helper
