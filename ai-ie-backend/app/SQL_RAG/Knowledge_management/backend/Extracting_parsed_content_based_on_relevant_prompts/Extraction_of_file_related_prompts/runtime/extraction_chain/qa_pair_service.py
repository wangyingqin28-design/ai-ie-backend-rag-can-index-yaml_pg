# [2026-07-04 10:18:20] 作用：导入 JSON 解析器；理由依据：DeepSeek 问答结果以 JSON 字符串返回。
import json
# [2026-07-04 10:18:20] 作用：导入正则表达式；理由依据：需移除模型可能附加的 Markdown 代码围栏。
import re
# [2026-07-04 10:18:20] 作用：导入当前时间；理由依据：每条问答必须记录 in_time。
from datetime import datetime
# [2026-07-04 10:18:20] 作用：导入 JSON 解码异常；理由依据：模型输出不完整时需要安全降级解析。
from json import JSONDecodeError
# [2026-07-04 10:18:20] 作用：导入任意值类型；理由依据：模型字段在校验前可能为字符串、整数或嵌套对象。
from typing import Any
# [2026-07-04 10:18:20] 作用：导入同步会话组件；理由依据：沿用原项目事务边界并支持测试替换。
from sqlalchemy.orm import Session, sessionmaker
# [2026-07-04 10:18:20] 作用：导入公共同步数据库引擎；理由依据：三表必须写入同一 PostgreSQL 实例。
from app.config import sync_engine
# [2026-07-04 10:18:20] 作用：导入问答 ORM；理由依据：本服务只负责 AI_Wendajilu 记录。
from extraction_chain.erp_ai_models import ErpWendaJilu
# [2026-07-04 10:18:20] 作用：导入 UUID7 生成器；理由依据：每条问答需要独立业务 ID。
from extraction_chain.snowflake_generator import generate_uuid7_id

# [2026-07-04 10:18:20] 作用：声明 Markdown 围栏清理函数；理由依据：兼容模型返回 ```json 包裹但不修改 JSON 内容。
def _strip_markdown_fence(text: str) -> str:
    # [2026-07-04 10:18:20] 作用：标准化输入并去除首尾空白；理由依据：空白不应影响 JSON 解码。
    cleaned = (text or "").strip()
    # [2026-07-04 10:18:20] 作用：移除开头 json 围栏；理由依据：部分兼容 API 会忽略“只输出 JSON”要求。
    cleaned = re.sub(r"^```json\s*", "", cleaned, flags=re.IGNORECASE)
    # [2026-07-04 10:18:20] 作用：移除开头普通围栏；理由依据：兼容未标注语言的代码块。
    cleaned = re.sub(r"^```\s*", "", cleaned)
    # [2026-07-04 10:18:20] 作用：移除末尾围栏；理由依据：保证剩余文本可交给 JSON 解码器。
    cleaned = re.sub(r"\s*```$", "", cleaned)
    # [2026-07-04 10:18:20] 作用：返回最终 JSON 候选文本；理由依据：后续解析只处理净化结果。
    return cleaned.strip()

# [2026-07-04 10:18:20] 作用：声明问答模型结果解析入口；理由依据：入库前必须把返回值规范成字典列表。
def parse_ai_qa_result(analysis: str) -> list[dict[str, Any]]:
    # [2026-07-04 10:18:20] 作用：处理空模型返回；理由依据：空结果不应生成伪问答。
    if not analysis:
        # [2026-07-04 10:18:20] 作用：返回空问答列表；理由依据：调用方据此跳过入库。
        return []
    # [2026-07-04 10:18:20] 作用：清理模型返回围栏；理由依据：提高合法 JSON 的兼容性。
    text = _strip_markdown_fence(analysis)
    # [2026-07-04 10:18:20] 作用：开始优先解析完整 JSON；理由依据：标准输出应直接是数组。
    try:
        # [2026-07-04 10:18:20] 作用：解码完整 JSON 文本；理由依据：保留模型输出字段和值。
        data = json.loads(text)
    # [2026-07-04 10:18:20] 作用：捕获模型附加非 JSON 前后缀；理由依据：需要从第一个 JSON 对象位置尝试恢复。
    except JSONDecodeError:
        # [2026-07-04 10:18:20] 作用：创建可从偏移位置解码的解析器；理由依据：raw_decode 能忽略 JSON 后缀说明。
        decoder = json.JSONDecoder()
        # [2026-07-04 10:18:20] 作用：收集数组或对象起点；理由依据：模型可能返回单对象或数组。
        starts = [position for position in (text.find("["), text.find("{")) if position != -1]
        # [2026-07-04 10:18:20] 作用：检测完全没有 JSON 起点；理由依据：不可恢复内容不能入库。
        if not starts:
            # [2026-07-04 10:18:20] 作用：返回空结果；理由依据：避免把自然语言误当结构化问答。
            return []
        # [2026-07-04 10:18:20] 作用：选择最早 JSON 起点；理由依据：保留模型返回的首个完整结构。
        start = min(starts)
        # [2026-07-04 10:18:20] 作用：开始从 JSON 起点恢复解析；理由依据：兼容前置说明文字。
        try:
            # [2026-07-04 10:18:20] 作用：解码首个 JSON 值；理由依据：忽略其后的非结构化尾注。
            data, _ = decoder.raw_decode(text[start:])
        # [2026-07-04 10:18:20] 作用：捕获仍不可恢复的 JSON；理由依据：错误结构不能进入数据库。
        except JSONDecodeError:
            # [2026-07-04 10:18:20] 作用：返回空结果；理由依据：由上层报告未提取到问答。
            return []
    # [2026-07-04 10:18:20] 作用：把单个问答对象规范成列表；理由依据：保存循环只处理统一列表接口。
    if isinstance(data, dict):
        # [2026-07-04 10:18:20] 作用：包装单问答对象；理由依据：兼容只有一个问题的模型返回。
        data = [data]
    # [2026-07-04 10:18:20] 作用：拒绝非列表顶层结构；理由依据：字符串或数字没有可映射字段。
    if not isinstance(data, list):
        # [2026-07-04 10:18:20] 作用：返回空结果；理由依据：阻止错误类型进入保存服务。
        return []
    # [2026-07-04 10:18:20] 作用：仅保留字典问答项；理由依据：每项必须能按字段名读取。
    return [item for item in data if isinstance(item, dict)]

# [2026-07-04 10:18:20] 作用：声明问答证据拆分函数；理由依据：客户问题原文和客服答案原文必须进入不同列。
def _extract_evidence(item: dict[str, Any]) -> tuple[str | None, str | None]:
    # [2026-07-04 10:18:20] 作用：读取证据字段并为空值提供空对象；理由依据：避免对 None 执行字典访问。
    evidence = item.get("evidence") or {}
    # [2026-07-04 10:18:20] 作用：兼容旧版字符串证据；理由依据：原项目曾允许单段证据文本。
    if isinstance(evidence, str):
        # [2026-07-04 10:18:20] 作用：把旧字符串同时用于两侧证据；理由依据：不丢弃已有模型输出。
        return evidence, evidence
    # [2026-07-04 10:18:20] 作用：处理标准嵌套证据对象；理由依据：当前提示词明确返回 customer_text/service_text。
    if isinstance(evidence, dict):
        # [2026-07-04 10:18:20] 作用：分别返回客户与客服证据；理由依据：防止 WenTiYuanWen 与 DaAnYuanWen 错位。
        return evidence.get("customer_text"), evidence.get("service_text")
    # [2026-07-04 10:18:20] 作用：处理无法识别的证据类型；理由依据：不能凭空构造原文。
    return None, None

# [2026-07-04 10:18:20] 作用：声明答案完整度到状态码转换；理由依据：ZhuangTai 使用数据库整数枚举。
def _status_to_int(value: Any) -> int:
    # [2026-07-04 10:18:20] 作用：为空完整度设置待审核状态；理由依据：缺少判断时不能宣称答案完整。
    if value is None:
        # [2026-07-04 10:18:20] 作用：返回待审核状态 0；理由依据：沿用原项目状态约定。
        return 0
    # [2026-07-04 10:18:20] 作用：接受已经是整数的状态；理由依据：兼容人工或上游直接提供状态码。
    if isinstance(value, int):
        # [2026-07-04 10:18:20] 作用：原样返回整数状态；理由依据：避免二次字符串转换。
        return value
    # [2026-07-04 10:18:20] 作用：定义业务状态映射；理由依据：字段真值表规定完整/部分完整/不完整/未明确为 1/2/3/4。
    mapping = {"待审核": 0, "完整": 1, "部分完整": 2, "不完整": 3, "未明确": 4, "在用": 1, "弃用": 2}
    # [2026-07-04 10:18:20] 作用：返回标准状态或默认待审核；理由依据：未知文本不能误标为已通过。
    return mapping.get(str(value).strip(), 0)

# [2026-07-04 10:18:20] 作用：声明问答批量保存入口；理由依据：把 DeepSeek 结构化问答逐条写入 AI_Wendajilu。
def save_qa_pairs(
    # [2026-07-04 10:18:20] 作用：强制使用关键字参数；理由依据：防止多个字符串 ID 和路径位置错位。
    *,
    # [2026-07-04 10:18:20] 作用：接收问答 JSON 字符串；理由依据：来源为三轮提取链的 qa_analysis。
    analysis: str,
    # [2026-07-04 10:18:20] 作用：接收原始数据 ID；理由依据：每条问答必须关联本次转录。
    raw_data_id: str | None = None,
    # [2026-07-04 10:18:20] 作用：保留原项目来源路径参数；理由依据：执行链签名兼容且不在问答表重复存储。
    source_file_path: str | None = None,
    # [2026-07-04 10:18:20] 作用：保留原项目文件类型参数；理由依据：执行链签名兼容且来源类型已在原始表保存。
    file_type: str | None = None,
    # [2026-07-04 10:18:20] 作用：接收企业 ID；理由依据：当前无企业上下文时保存 NULL。
    gs_id: str | None = None,
    # [2026-07-04 10:18:20] 作用：接收录入用户 ID；理由依据：当前无登录上下文时保存 NULL。
    in_userid: str | None = None,
# [2026-07-04 10:18:20] 作用：结束保存入口签名并声明返回 ID 列表；理由依据：API 需用这些 ID 做数据库验收。
) -> list[str]:
    # [2026-07-04 10:18:20] 作用：解析 DeepSeek 问答结果；理由依据：保存前必须取得字典字段。
    qa_items = parse_ai_qa_result(analysis)
    # [2026-07-04 10:18:20] 作用：验证问答和原始关联均存在；理由依据：不允许生成无来源明细。
    if not qa_items or not raw_data_id:
        # [2026-07-04 10:18:20] 作用：返回空 ID 集合；理由依据：明确表示没有写入记录。
        return []
    # [2026-07-04 10:18:20] 作用：创建同步会话工厂；理由依据：保持原项目事务语义。
    SessionLocal = sessionmaker(bind=sync_engine, class_=Session, expire_on_commit=False)
    # [2026-07-04 10:18:20] 作用：初始化已保存问答 ID；理由依据：响应需返回实际入库主键。
    saved_ids: list[str] = []
    # [2026-07-04 10:18:20] 作用：自动管理数据库会话；理由依据：事务结束后释放连接。
    with SessionLocal() as db:
        # [2026-07-04 10:18:20] 作用：开始问答批量事务；理由依据：任一条失败时整批回滚。
        try:
            # [2026-07-04 10:18:20] 作用：逐条处理问答项；理由依据：一个对话可拆分多个独立问题。
            for item in qa_items:
                # [2026-07-04 10:18:20] 作用：拆分问题与答案证据；理由依据：两类原文必须写入各自列。
                customer_text, service_text = _extract_evidence(item)
                # [2026-07-04 10:18:20] 作用：生成问答 UUID7；理由依据：每条知识需要唯一主键。
                qa_id = generate_uuid7_id()
                # [2026-07-04 10:18:20] 作用：构造完整问答记录；理由依据：字段真值表要求业务、状态、审计、保留列全部显式赋值。
                record = ErpWendaJilu(
                    # [2026-07-04 10:18:20] 作用：写入问答 UUID7；理由依据：形成复合主键第一部分。
                    wdjl_id=qa_id,
                    # [2026-07-04 10:18:20] 作用：写入原始数据 ID；理由依据：形成复合主键第二部分并关联全文。
                    Yssj_id=raw_data_id,
                    # [2026-07-04 10:18:20] 作用：写入客户原问题；理由依据：来源为 question。
                    AI_WenTi=item.get("question"),
                    # [2026-07-04 10:18:20] 作用：写入客服答案；理由依据：来源为 answer。
                    AI_DaAn=item.get("answer"),
                    # [2026-07-04 10:18:20] 作用：写入问题场景；理由依据：来源为 question_scene，不能混入 description。
                    AI_Biaozhu=item.get("question_scene"),
                    # [2026-07-04 10:18:20] 作用：写入问题证据原文；理由依据：来源为 evidence.customer_text。
                    WenTiYuanWen=customer_text,
                    # [2026-07-04 10:18:20] 作用：写入答案证据原文；理由依据：来源为 evidence.service_text。
                    DaAnYuanWen=service_text,
                    # [2026-07-04 10:18:20] 作用：写入标准知识问题；理由依据：优先使用 standard_question，旧结果缺失时才回退 question。
                    WenTi_true=item.get("standard_question") or item.get("question"),
                    # [2026-07-04 10:18:20] 作用：写入当前确认答案；理由依据：尚无人工修改时等于 DeepSeek answer。
                    DaAn_true=item.get("answer"),
                    # [2026-07-04 10:18:20] 作用：写入检索语义描述；理由依据：来源为第二轮描述提示词 description。
                    Biaozhu_true=item.get("description"),
                    # [2026-07-04 10:18:20] 作用：写入答案完整度状态；理由依据：优先读取 answer_completeness 并兼容旧 status。
                    ZhuangTai=_status_to_int(item.get("answer_completeness") or item.get("status")),
                    # [2026-07-04 10:18:20] 作用：显式保存未审核人；理由依据：新记录尚未发生人工审核。
                    ZhuangTai_id=None,
                    # [2026-07-04 10:18:20] 作用：显式保存未审核时间；理由依据：新记录尚未发生人工审核。
                    ZhuangTai_time=None,
                    # [2026-07-04 10:18:20] 作用：写入音频时间区间；理由依据：来源为 DeepSeek time。
                    YinPinShiJian=item.get("time"),
                    # [2026-07-04 10:18:20] 作用：写入企业 ID；理由依据：无企业上下文时保持 NULL。
                    gsId=gs_id,
                    # [2026-07-04 10:18:20] 作用：写入录入用户 ID；理由依据：无登录上下文时保持 NULL。
                    in_userid=in_userid,
                    # [2026-07-04 10:18:20] 作用：写入当前录入时间；理由依据：用于测试窗口和审计。
                    in_time=datetime.now(),
                    # [2026-07-04 10:18:20] 作用：显式保存保留列为空；理由依据：原项目无 yima 业务赋值且现有记录均为空。
                    yima=None,
                # [2026-07-04 10:18:20] 作用：结束问答记录构造；理由依据：形成完整 ORM 实例。
                )
                # [2026-07-04 10:18:20] 作用：把问答记录加入事务；理由依据：等待整批统一提交。
                db.add(record)
                # [2026-07-04 10:18:20] 作用：记录已生成问答 ID；理由依据：提交成功后返回给 API 验收。
                saved_ids.append(qa_id)
            # [2026-07-04 10:18:20] 作用：提交问答批量事务；理由依据：确保所有字段一次落库。
            db.commit()
            # [2026-07-04 10:18:20] 作用：返回问答 ID 列表；理由依据：调用方需按 ID 核验数据库行。
            return saved_ids
        # [2026-07-04 10:18:20] 作用：捕获任意问答入库异常；理由依据：禁止部分成功造成字段或数量不一致。
        except Exception:
            # [2026-07-04 10:18:20] 作用：回滚问答事务；理由依据：维护整批一致性。
            db.rollback()
            # [2026-07-04 10:18:20] 作用：重新抛出真实异常；理由依据：API 和日志必须显示失败而非模拟成功。
            raise
