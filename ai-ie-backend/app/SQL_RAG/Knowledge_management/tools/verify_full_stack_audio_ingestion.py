# [2026-07-04 10:18:20] 作用：导入命令行参数解析器；理由依据：验收器需要接收录音、报告、客户和可选数据库 IPv4 地址。
import argparse
# [2026-07-04 10:18:20] 作用：导入文件哈希算法；理由依据：脱敏报告必须用 SHA256 唯一标识被测录音。
import hashlib
# [2026-07-04 10:18:20] 作用：导入 JSON 序列化工具；理由依据：命令行需要输出机器可读的脱敏验收摘要。
import json
# [2026-07-04 10:18:20] 作用：导入环境变量操作；理由依据：可在加载 Pydantic 配置前指定数据库 IPv4，规避主机名优先解析不可达 IPv6。
import os
# [2026-07-04 10:18:20] 作用：导入模块搜索路径控制；理由依据：工具目录直接执行时需显式加入 backend 才能加载 knowledge_api。
import sys
# [2026-07-04 10:18:20] 作用：导入时间工具；理由依据：报告需要精确记录本轮真实验收时间。
from datetime import datetime
# [2026-07-04 10:18:20] 作用：导入路径对象；理由依据：稳定定位 Knowledge 根目录、音频和报告文件。
from pathlib import Path
# [2026-07-04 10:18:20] 作用：导入 URL 解析器；理由依据：报告只保留实际代理端口而不写入完整连接信息。
from urllib.parse import urlparse
# [2026-07-04 10:18:20] 作用：导入 HTTP 客户端；理由依据：通过 18321 WebUI 同源代理发送真实 multipart 音频并执行健康检查。
import httpx
# [2026-07-04 10:18:20] 作用：计算 Knowledge_management 根目录；理由依据：工具文件固定存放在根目录下的 tools 子目录。
KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
# [2026-07-04 10:18:20] 作用：计算知识库 backend 根目录；理由依据：直接执行脚本时 Python 默认不会把该目录加入包搜索路径。
BACKEND_ROOT = KNOWLEDGE_ROOT / "backend"
# [2026-07-04 10:18:20] 作用：把 backend 插入模块搜索路径首位；理由依据：确保加载本次迁移后的 knowledge_api 和 extraction_chain。
sys.path.insert(0, str(BACKEND_ROOT))
# [2026-07-04 10:18:20] 作用：导入统一运行时初始化函数；理由依据：真实 API 与验收器必须使用相同公共配置、模型和数据库上下文。
from knowledge_api.runtime_paths import configure_runtime_paths
# [2026-07-04 10:18:20] 作用：声明默认 WebUI 代理上传地址；理由依据：用户要求两条业务链通过新前端端口串联而不是绕过代理。
DEFAULT_ENDPOINT = "http://127.0.0.1:18321/api/knowledge/parse"
# [2026-07-04 10:18:20] 作用：声明脱敏报告允许的顶层字段白名单；理由依据：禁止把全文、密钥、密码或连接串写入验收文件。
SAFE_REPORT_KEYS = frozenset({"verified_at", "audio_sha256", "audio_size", "backend_port", "web_port", "transcription_model", "llm_model", "direct_health", "web_health", "proxy_health", "asset_type_id", "customer_id", "raw_data_id", "qa_pair_ids", "intent_ids", "pre_counts", "post_counts", "deltas", "transcript_length", "field_checks", "schema_checks"})
# [2026-07-04 10:18:20] 作用：声明三个目标数据表名称；理由依据：验收必须覆盖原始转录、问答知识和意图知识全部写库结果。
TARGET_TABLES = ("AI_YuanShishuju", "AI_Wendajilu", "AI_Yitu")
# [2026-07-04 10:18:20] 作用：构造命令行参数解析器；理由依据：保持真实测试输入明确、可复现且不硬编码动态数据库地址。
def build_parser() -> argparse.ArgumentParser:
    # [2026-07-04 10:18:20] 作用：创建验收器参数解析器；理由依据：帮助信息需要说明脚本执行真实外部 API 和保留入库记录。
    parser = argparse.ArgumentParser(description="Verify retained Knowledge audio ingestion through the WebUI proxy.")
    # [2026-07-04 10:18:20] 作用：声明必填录音文件参数；理由依据：只能对用户指定的真实 M4A 计算哈希并上传。
    parser.add_argument("--audio", required=True, type=Path)
    # [2026-07-04 10:18:20] 作用：声明可覆盖的代理端点；理由依据：默认固定 18321，同时支持脚本明确报告的已验证回退端口。
    parser.add_argument("--endpoint", default=DEFAULT_ENDPOINT)
    # [2026-07-04 10:18:20] 作用：声明脱敏报告输出路径；理由依据：最终证据需保存在 Knowledge_management 内供用户复核。
    parser.add_argument("--report", type=Path, default=KNOWLEDGE_ROOT / "VERIFICATION_REPORT_2026-07-04.md")
    # [2026-07-04 10:18:20] 作用：声明本轮测试客户标识；理由依据：验证 GuanLianKeHu 接收显式业务值且不与其他字段错位。
    parser.add_argument("--customer-id", default="20260704")
    # [2026-07-04 10:18:20] 作用：声明可选数据库主机覆盖；理由依据：Windows 主机名可能优先返回不可达 IPv6，验收可指定同机真实 IPv4。
    parser.add_argument("--database-host")
    # [2026-07-04 10:18:20] 作用：返回配置完成的解析器；理由依据：主入口统一解析所有运行参数。
    return parser
# [2026-07-04 10:18:20] 作用：计算文件 SHA256；理由依据：报告用固定哈希证明实际上传的是指定录音而不保存录音内容。
def sha256_file(path: Path) -> str:
    # [2026-07-04 10:18:20] 作用：创建 SHA256 增量计算器；理由依据：避免一次性把较大音频全部读入内存。
    digest = hashlib.sha256()
    # [2026-07-04 10:18:20] 作用：以二进制方式打开录音；理由依据：哈希必须基于原始字节而不能发生文本编码转换。
    with path.open("rb") as stream:
        # [2026-07-04 10:18:20] 作用：循环读取固定大小的音频块；理由依据：保持内存占用稳定并覆盖完整文件。
        while chunk := stream.read(1024 * 1024):
            # [2026-07-04 10:18:20] 作用：把当前音频块加入哈希；理由依据：最终摘要必须覆盖每一个上传字节。
            digest.update(chunk)
    # [2026-07-04 10:18:20] 作用：返回十六进制 SHA256；理由依据：报告需要通用可复核的文件标识格式。
    return digest.hexdigest()
# [2026-07-04 10:18:20] 作用：断言业务值为非空文本；理由依据：字段存在但仅包含空白仍属于提取或映射失败。
def require_text(value: object, field_name: str) -> None:
    # [2026-07-04 10:18:20] 作用：拒绝非字符串或空白字段；理由依据：问答、意图、证据、时间和转录均要求真实内容。
    if not isinstance(value, str) or not value.strip():
        # [2026-07-04 10:18:20] 作用：抛出带字段名的验收错误；理由依据：失败报告需能精确定位错入或漏入列。
        raise AssertionError(f"字段为空或类型错误: {field_name}")
# [2026-07-04 10:18:20] 作用：读取三张表当前行数；理由依据：真实测试前后计数差必须等于 API 返回的写入数量。
def read_counts(connection, text) -> dict[str, int]:
    # [2026-07-04 10:18:20] 作用：逐表执行只读计数查询；理由依据：不执行清理操作并分别验证三类记录增量。
    return {table: connection.execute(text(f'SELECT COUNT(*) FROM "{table}"')).scalar_one() for table in TARGET_TABLES}
# [2026-07-04 10:18:20] 作用：从真实资产类型表选择一个在用主键；理由依据：ZcLeiXin 必须引用现有 AI_ZiChanLeiXing.zclxId，不能写入虚构测试值。
def select_asset_type_id(connection, text) -> str:
    # [2026-07-04 10:18:20] 作用：查询首个未删除且在用的资产类型主键；理由依据：选择逻辑需排除已删除资产并保持测试确定性。
    asset_id = connection.execute(text('SELECT "zclxId" FROM "AI_ZiChanLeiXing" WHERE del_flag=false AND "zhuangTai"=:status ORDER BY "zclxId" LIMIT 1'), {"status": "在用"}).scalar_one()
    # [2026-07-04 10:18:20] 作用：验证选出的资产主键非空；理由依据：空主键会导致原始数据 ZcLeiXin 失去业务关联。
    require_text(asset_id, "AI_ZiChanLeiXing.zclxId")
    # [2026-07-04 10:18:20] 作用：返回真实资产类型主键；理由依据：同一个值用于 multipart 元数据和数据库等值断言。
    return asset_id
# [2026-07-04 10:18:20] 作用：核对 ORM 列集合与直播数据库列集合；理由依据：代码模型少列或多列都会造成字段漏入、错入或查询异常。
def validate_schema(connection, inspect, models: dict[str, object]) -> dict[str, bool]:
    # [2026-07-04 10:18:20] 作用：创建当前连接的数据库反射器；理由依据：必须读取本次实际 PostgreSQL 结构而非依赖截图推断。
    inspector = inspect(connection)
    # [2026-07-04 10:18:20] 作用：初始化逐表结构核验结果；理由依据：脱敏报告只记录布尔值而不泄露数据库连接信息。
    checks: dict[str, bool] = {}
    # [2026-07-04 10:18:20] 作用：遍历三张表与对应 ORM；理由依据：任何一张表都不能跳过完整列集合比较。
    for table_name, model in models.items():
        # [2026-07-04 10:18:20] 作用：读取 ORM 映射的真实列名集合；理由依据：包含带空格的引号主键和大小写敏感字段。
        orm_columns = {column.name for column in model.__table__.columns}
        # [2026-07-04 10:18:20] 作用：读取 PostgreSQL 反射列名集合；理由依据：以直播数据库为字段完整性的最终依据。
        database_columns = {column["name"] for column in inspector.get_columns(table_name)}
        # [2026-07-04 10:18:20] 作用：记录两套列集合是否完全相等；理由依据：仅检查包含关系会掩盖额外或遗漏字段。
        checks[table_name] = orm_columns == database_columns
        # [2026-07-04 10:18:20] 作用：在列集合不一致时立即终止验收；理由依据：结构不匹配时继续写库不能给出字段正确结论。
        if not checks[table_name]:
            # [2026-07-04 10:18:20] 作用：报告缺失和多余列名；理由依据：便于精确修复 ORM，同时不包含任何敏感连接数据。
            raise AssertionError(f"{table_name} ORM/数据库列不一致: missing={sorted(database_columns-orm_columns)}, extra={sorted(orm_columns-database_columns)}")
    # [2026-07-04 10:18:20] 作用：返回逐表结构布尔结果；理由依据：脱敏报告需要保留三表全量字段覆盖证据。
    return checks
# [2026-07-04 10:18:20] 作用：通过 WebUI 代理上传真实音频；理由依据：端到端测试必须覆盖 multipart 转发、SiliconFlow 转写、DeepSeek 提取和数据库保存。
def upload_audio(client: httpx.Client, endpoint: str, audio: Path, asset_id: str, customer_id: str) -> dict[str, object]:
    # [2026-07-04 10:18:20] 作用：以二进制方式打开真实录音；理由依据：multipart 文件内容必须与哈希所对应字节完全一致。
    with audio.open("rb") as stream:
        # [2026-07-04 10:18:20] 作用：向 18321 同源代理发送文件和业务元数据；理由依据：验证前端代理没有丢失边界、资产类型或客户字段。
        response = client.post(endpoint, files={"file": (audio.name, stream, "audio/mp4")}, data={"asset_type_id": asset_id, "customer_id": customer_id})
    # [2026-07-04 10:18:20] 作用：要求代理返回成功 HTTP 状态；理由依据：外部 API 或保存失败必须以非零验收退出而不能吞错。
    response.raise_for_status()
    # [2026-07-04 10:18:20] 作用：解析 WebUI 合同 JSON；理由依据：后续数据库查询以返回主键为唯一范围。
    payload = response.json()
    # [2026-07-04 10:18:20] 作用：验证原始数据主键非空；理由依据：缺少 rawDataId 无法关联问答和意图记录。
    require_text(payload.get("rawDataId"), "rawDataId")
    # [2026-07-04 10:18:20] 作用：验证至少返回一个问答主键；理由依据：用户要求提示词提取问答内容并入库。
    if not payload.get("qaPairIds"):
        # [2026-07-04 10:18:20] 作用：报告问答主键缺失；理由依据：不能把只有转录或意图的部分链路判为成功。
        raise AssertionError("qaPairIds 为空")
    # [2026-07-04 10:18:20] 作用：验证至少返回一个意图主键；理由依据：第五张截图对应 AI_Yitu 字段也必须有新记录。
    if not payload.get("intentIds"):
        # [2026-07-04 10:18:20] 作用：报告意图主键缺失；理由依据：不能把只有转录或问答的部分链路判为成功。
        raise AssertionError("intentIds 为空")
    # [2026-07-04 10:18:20] 作用：验证返回转录全文非空；理由依据：SiliconFlow 文件解析结果是两轮 DeepSeek 提取的输入依据。
    require_text(payload.get("fullText"), "fullText")
    # [2026-07-04 10:18:20] 作用：返回已通过基础合同校验的响应；理由依据：数据库验收只消费可信主键和长度信息。
    return payload
# [2026-07-04 10:18:20] 作用：查询并验证本轮三表所有字段；理由依据：返回 ID 不等于字段正确，必须逐列核对值、关联和空值语义。
def validate_rows(connection, text, payload: dict[str, object], asset_id: str, customer_id: str) -> dict[str, bool]:
    # [2026-07-04 10:18:20] 作用：读取返回的原始数据主键；理由依据：三表查询严格限定本轮新记录。
    raw_id = str(payload["rawDataId"])
    # [2026-07-04 10:18:20] 作用：按主键查询唯一原始数据行；理由依据：验证完整转录与文件元数据实际持久化。
    raw = dict(connection.execute(text('SELECT * FROM "AI_YuanShishuju" WHERE shuju_id=:id'), {"id": raw_id}).mappings().one())
    # [2026-07-04 10:18:20] 作用：按外键查询本轮全部问答行；理由依据：检查每个返回问答 ID 都关联同一原始数据。
    qa_rows = [dict(row) for row in connection.execute(text('SELECT * FROM "AI_Wendajilu" WHERE "Yssj_id"=:id'), {"id": raw_id}).mappings()]
    # [2026-07-04 10:18:20] 作用：按外键查询本轮全部意图行；理由依据：检查每个返回意图 ID 都关联同一原始数据。
    intent_rows = [dict(row) for row in connection.execute(text('SELECT * FROM "AI_Yitu" WHERE "Yssj_id"=:id'), {"id": raw_id}).mappings()]
    # [2026-07-04 10:18:20] 作用：断言数据库问答主键与 API 返回集合完全相等；理由依据：防止漏写、重复写或错误关联历史记录。
    assert {row["wdjl_ id"] for row in qa_rows} == set(payload["qaPairIds"])
    # [2026-07-04 10:18:20] 作用：断言数据库意图主键与 API 返回集合完全相等；理由依据：防止漏写、重复写或错误关联历史记录。
    assert {row["yt_ id"] for row in intent_rows} == set(payload["intentIds"])
    # [2026-07-04 10:18:20] 作用：逐项验证原始数据业务值、审计值和预留空值；理由依据：第三张截图对应的源记录必须完整且不把未知值伪造进库。
    raw_ok = raw["shuju_id"] == raw_id and raw["ZcLeiXin"] == asset_id and raw["ShuJu"] == payload["fullText"] and bool(raw["WenJianDiZhi"]) and raw["WenJianName"] == Path(str(payload["fileName"])).name and raw["LaiYuan"] == 3 and raw["GuanLianKeHu"] == customer_id and raw["gs_id"] is None and raw["del_flag"] is False and raw["del_time"] is None and raw["in_userid"] is None and raw["in_time"] is not None and raw["up_userid"] is None and raw["up_time"] is None and raw["yima"] is None
    # [2026-07-04 10:18:20] 作用：逐行验证问答问题、答案、场景、证据、标准字段、状态、时间及预留字段；理由依据：避免原问题与标准问题错位或证据漏入。
    qa_ok = all(row["Yssj_id"] == raw_id and all(isinstance(row[field], str) and row[field].strip() for field in ("AI_WenTi", "AI_DaAn", "AI_Biaozhu", "WenTiYuanWen", "DaAnYuanWen", "WenTi_true", "DaAn_true", "Biaozhu_true", "YinPinShiJian")) and row["ZhuangTai"] in {0, 1, 2, 3} and row["ZhuangTai_id"] is None and row["ZhuangTai_time"] is None and row["gsId"] is None and row["in_userid"] is None and row["in_time"] is not None and row["yima"] is None for row in qa_rows)
    # [2026-07-04 10:18:20] 作用：逐行验证意图、描述、证据、状态、时间及预留字段；理由依据：第五张截图中的 AI_Yitu 每个业务字段都必须来自正确提取键。
    intent_ok = all(row["Yssj_id"] == raw_id and all(isinstance(row[field], str) and row[field].strip() for field in ("AI_YiTu", "YiTu", "BiaoZhu", "ShiJian")) and row["ZhuangTai"] == 0 and row["ZhuangTai_id"] is None and row["ZhuangTai_time"] is None and row["gsId"] is None and row["del_time"] is None and row["in_userid"] is None and row["in_time"] is not None and row["yima"] is None for row in intent_rows)
    # [2026-07-04 10:18:20] 作用：汇总三类逐字段核验布尔值；理由依据：报告只保存通过状态而不泄露转录、问答或意图正文。
    checks = {"raw_all_fields": raw_ok, "qa_all_fields": qa_ok, "intent_all_fields": intent_ok, "child_foreign_keys": all(row["Yssj_id"] == raw_id for row in qa_rows + intent_rows)}
    # [2026-07-04 10:18:20] 作用：在任一字段规则失败时终止验收；理由依据：用户明确禁止错入、漏入后仍报告跑通。
    if not all(checks.values()):
        # [2026-07-04 10:18:20] 作用：报告失败布尔项但不打印正文；理由依据：兼顾可诊断性与脱敏要求。
        raise AssertionError(f"三表字段核验失败: {checks}")
    # [2026-07-04 10:18:20] 作用：返回三表字段核验结果；理由依据：写入最终脱敏报告作为逐列通过证据。
    return checks
# [2026-07-04 10:18:20] 作用：检查报告文本不含敏感连接信息；理由依据：即使报告字段白名单正确，也需阻止意外字符串注入。
def assert_report_is_redacted(report_text: str) -> None:
    # [2026-07-04 10:18:20] 作用：把报告转换为小写用于大小写无关扫描；理由依据：敏感标记可能采用不同大小写。
    lowered = report_text.lower()
    # [2026-07-04 10:18:20] 作用：声明禁止出现在报告中的密钥和连接标记；理由依据：API Key、密码和完整数据库 URL 均不得落盘。
    forbidden = ("api_key", "password=", "postgresql://", "postgresql+", "sk-")
    # [2026-07-04 10:18:20] 作用：逐个断言敏感标记不存在；理由依据：发现任何泄露风险都应阻止报告写入。
    if any(marker in lowered for marker in forbidden):
        # [2026-07-04 10:18:20] 作用：抛出脱敏失败错误；理由依据：安全约束优先于生成验收文件。
        raise AssertionError("报告包含被禁止的敏感连接或密钥标记")
# [2026-07-04 10:18:20] 作用：把安全字段写成 Markdown 报告；理由依据：用户需要可阅读的端口、模型、ID、计数和逐项布尔证据。
def write_report(path: Path, report: dict[str, object]) -> None:
    # [2026-07-04 10:18:20] 作用：断言报告没有超出白名单的顶层字段；理由依据：防止未来维护时误把响应全文或配置对象加入报告。
    assert set(report) <= SAFE_REPORT_KEYS
    # [2026-07-04 10:18:20] 作用：将安全报告数据编码为格式化 JSON；理由依据：Markdown 代码块便于人工与机器复核且不保存业务正文。
    safe_json = json.dumps(report, ensure_ascii=False, indent=2)
    # [2026-07-04 10:18:20] 作用：构造带结论说明的 Markdown 文本；理由依据：明确本轮记录保留且报告已经脱敏。
    text = "# 文件解析与 DeepSeek 提取入库最终验证报告\n\n本报告仅包含脱敏验收元数据；本轮数据库记录已保留。\n\n```json\n" + safe_json + "\n```\n"
    # [2026-07-04 10:18:20] 作用：在落盘前执行敏感内容扫描；理由依据：安全检查失败时不得产生部分报告。
    assert_report_is_redacted(text)
    # [2026-07-04 10:18:20] 作用：确保报告父目录存在；理由依据：允许用户指定 Knowledge 根目录下的新报告位置。
    path.parent.mkdir(parents=True, exist_ok=True)
    # [2026-07-04 10:18:20] 作用：以 UTF-8 写入脱敏报告；理由依据：中文说明和模型名必须保持可读。
    path.write_text(text, encoding="utf-8")
# [2026-07-04 10:18:20] 作用：执行完整真实验收并返回脱敏结果；理由依据：把健康、上传、结构、字段、计数和报告生成串成单一失败即退出流程。
def run(args: argparse.Namespace) -> dict[str, object]:
    # [2026-07-04 10:18:20] 作用：解析并验证真实录音绝对路径；理由依据：不存在或空文件不能调用外部解析服务。
    audio = args.audio.resolve()
    # [2026-07-04 10:18:20] 作用：拒绝不存在或零字节的录音；理由依据：确保 SiliconFlow 接收可解析的真实 M4A 内容。
    if not audio.is_file() or audio.stat().st_size <= 0:
        # [2026-07-04 10:18:20] 作用：报告无效录音路径；理由依据：输入错误应在调用外部 API 前明确失败。
        raise FileNotFoundError(f"录音文件不存在或为空: {audio}")
    # [2026-07-04 10:18:20] 作用：在配置加载前应用可选数据库主机覆盖；理由依据：Pydantic 环境优先级可避免 Windows 选择不可达 IPv6。
    if args.database_host:
        # [2026-07-04 10:18:20] 作用：设置本进程 DB_HOST；理由依据：只影响验收连接，不改写用户保存的数据库密码或连接文件。
        os.environ["DB_HOST"] = args.database_host
    # [2026-07-04 10:18:20] 作用：初始化公共与提取运行时；理由依据：后续导入必须复用真实模型、配置和 ORM。
    configure_runtime_paths()
    # [2026-07-04 10:18:20] 作用：延迟导入 SQLAlchemy 反射和 SQL 文本；理由依据：先完成 Knowledge 专用运行时路径配置。
    from sqlalchemy import inspect, text
    # [2026-07-04 10:18:20] 作用：延迟导入真实数据库引擎与模型配置；理由依据：确保可选 DB_HOST 已在 Pydantic 初始化前生效。
    from app.config import settings, sync_engine
    # [2026-07-04 10:18:20] 作用：延迟导入三表 ORM 类；理由依据：结构核验必须使用本次迁移后的 extraction_chain 模型。
    from extraction_chain.erp_ai_models import ErpWendaJilu, ErpYitu, ErpYuanShiShuJu
    # [2026-07-04 10:18:20] 作用：建立数据库连接读取基线、真实资产主键和结构；理由依据：上传前状态用于精确计算本轮增量。
    with sync_engine.connect() as connection:
        # [2026-07-04 10:18:20] 作用：记录上传前三表行数；理由依据：最终计数增量必须与返回 ID 数量一一对应。
        pre_counts = read_counts(connection, text)
        # [2026-07-04 10:18:20] 作用：选择现有在用资产类型主键；理由依据：原始数据 ZcLeiXin 使用真实关联值。
        asset_id = select_asset_type_id(connection, text)
        # [2026-07-04 10:18:20] 作用：核对三表 ORM 与直播数据库列完全一致；理由依据：上传前先阻止结构不完整的写入。
        schema_checks = validate_schema(connection, inspect, {"AI_YuanShishuju": ErpYuanShiShuJu, "AI_Wendajilu": ErpWendaJilu, "AI_Yitu": ErpYitu})
    # [2026-07-04 10:18:20] 作用：创建十五分钟超时的 HTTP 客户端；理由依据：真实语音转写和两轮 DeepSeek 提取可能明显长于普通 API 请求。
    with httpx.Client(timeout=httpx.Timeout(900.0)) as client:
        # [2026-07-04 10:18:20] 作用：检查知识库后端直连健康；理由依据：确认密钥、模型和数据库在上传前均 ready。
        direct_health = client.get("http://127.0.0.1:18320/health").json().get("ready") is True
        # [2026-07-04 10:18:20] 作用：检查知识库 WebUI 自身健康；理由依据：用户访问的新前端服务必须正常监听。
        web_health = client.get("http://127.0.0.1:18321/health").json().get("ready") is True
        # [2026-07-04 10:18:20] 作用：通过 WebUI 同源代理检查后端健康；理由依据：证明代理目标与本次知识库后端已串联。
        proxy_health = client.get("http://127.0.0.1:18321/api/health").json().get("ready") is True
        # [2026-07-04 10:18:20] 作用：要求三项健康检查全部通过；理由依据：部分服务可用不能进入真实入库测试。
        assert direct_health and web_health and proxy_health
        # [2026-07-04 10:18:20] 作用：通过 WebUI 代理执行真实音频解析和提取；理由依据：覆盖用户指定的完整前后端调用路径。
        payload = upload_audio(client, args.endpoint, audio, asset_id, str(args.customer_id))
    # [2026-07-04 10:18:20] 作用：重新连接数据库查询本轮写入行；理由依据：提交后连接可见性和每列最终值必须在独立事务中核对。
    with sync_engine.connect() as connection:
        # [2026-07-04 10:18:20] 作用：验证三表全部字段和关联关系；理由依据：确保没有错入、漏入或预留字段伪造。
        field_checks = validate_rows(connection, text, payload, asset_id, str(args.customer_id))
        # [2026-07-04 10:18:20] 作用：记录上传后三表行数；理由依据：用于验证数据库增量与 API 返回数量相等。
        post_counts = read_counts(connection, text)
    # [2026-07-04 10:18:20] 作用：计算三表本轮行数增量；理由依据：识别隐藏的重复写入或漏写。
    deltas = {table: post_counts[table] - pre_counts[table] for table in TARGET_TABLES}
    # [2026-07-04 10:18:20] 作用：断言原始数据恰好新增一行；理由依据：完整转录必须保存为单条 TEXT 而不能再次按长度拆分。
    assert deltas["AI_YuanShishuju"] == 1
    # [2026-07-04 10:18:20] 作用：断言问答增量等于返回问答 ID 数；理由依据：确保每个 DeepSeek 问答结果只写一次。
    assert deltas["AI_Wendajilu"] == len(payload["qaPairIds"])
    # [2026-07-04 10:18:20] 作用：断言意图增量等于返回意图 ID 数；理由依据：确保每个 DeepSeek 意图结果只写一次。
    assert deltas["AI_Yitu"] == len(payload["intentIds"])
    # [2026-07-04 10:18:20] 作用：解析实际 WebUI 代理端口；理由依据：报告只保存端口数字而不保存完整 URL。
    web_port = urlparse(args.endpoint).port
    # [2026-07-04 10:18:20] 作用：构造白名单范围内的脱敏验收结果；理由依据：只记录模型、ID、计数、长度、布尔值、端口和文件哈希。
    report = {"verified_at": datetime.now().astimezone().isoformat(timespec="seconds"), "audio_sha256": sha256_file(audio), "audio_size": audio.stat().st_size, "backend_port": 18320, "web_port": web_port, "transcription_model": settings.AUDIO_TRANSCRIPTION_MODEL, "llm_model": settings.LLM_MODEL, "direct_health": direct_health, "web_health": web_health, "proxy_health": proxy_health, "asset_type_id": asset_id, "customer_id": str(args.customer_id), "raw_data_id": payload["rawDataId"], "qa_pair_ids": payload["qaPairIds"], "intent_ids": payload["intentIds"], "pre_counts": pre_counts, "post_counts": post_counts, "deltas": deltas, "transcript_length": len(str(payload["fullText"])), "field_checks": field_checks, "schema_checks": schema_checks}
    # [2026-07-04 10:18:20] 作用：写入最终脱敏验收报告；理由依据：为用户保留可重复核对且不泄露正文和凭据的证据。
    write_report(args.report.resolve(), report)
    # [2026-07-04 10:18:20] 作用：返回脱敏结果供命令行输出；理由依据：自动化调用可据此读取本轮主键和布尔结论。
    return report
# [2026-07-04 10:18:20] 作用：声明命令行主入口；理由依据：统一解析参数、执行验收并输出安全 JSON。
def main() -> int:
    # [2026-07-04 10:18:20] 作用：解析参数并运行完整验收；理由依据：任一异常自然产生非零退出码，防止虚假成功。
    report = run(build_parser().parse_args())
    # [2026-07-04 10:18:20] 作用：向终端输出脱敏报告数据；理由依据：执行者无需打开文件即可核对 ID、增量和布尔结果。
    print(json.dumps(report, ensure_ascii=False, indent=2))
    # [2026-07-04 10:18:20] 作用：返回成功退出码；理由依据：仅全部断言和报告写入完成后才到达此行。
    return 0
# [2026-07-04 10:18:20] 作用：检测脚本直接执行场景；理由依据：被契约测试导入时不得自动调用外部 API。
if __name__ == "__main__":
    # [2026-07-04 10:18:20] 作用：执行主入口并把结果传给操作系统；理由依据：PowerShell 可根据退出码判断真实验收是否成功。
    raise SystemExit(main())
