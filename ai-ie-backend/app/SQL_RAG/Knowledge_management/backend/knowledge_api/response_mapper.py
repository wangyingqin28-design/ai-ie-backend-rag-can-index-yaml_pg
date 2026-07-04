# [2026-07-04 10:18:20] 作用：导入 JSON 解码器；理由依据：process_service 返回问答和意图 JSON 字符串。
import json
# [2026-07-04 10:18:20] 作用：导入任意值类型；理由依据：处理结果包含字符串、列表和嵌套字典。
from typing import Any

# [2026-07-04 10:18:20] 作用：声明安全 JSON 列表解析函数；理由依据：映射层不能因空值或异常类型产生伪知识。
def _parse_items(value: Any) -> list[dict[str, Any]]:
    # [2026-07-04 10:18:20] 作用：直接接受字典列表；理由依据：兼容未来 process_service 返回已解析对象。
    if isinstance(value, list):
        # [2026-07-04 10:18:20] 作用：过滤列表中的非字典项；理由依据：知识卡片必须按字段名读取。
        return [item for item in value if isinstance(item, dict)]
    # [2026-07-04 10:18:20] 作用：拒绝空值和非字符串；理由依据：不能凭空生成知识内容。
    if not isinstance(value, str) or not value.strip():
        # [2026-07-04 10:18:20] 作用：返回空列表；理由依据：前端应看到真实空结果。
        return []
    # [2026-07-04 10:18:20] 作用：开始解码 JSON 字符串；理由依据：标准提取结果是 JSON 数组。
    try:
        # [2026-07-04 10:18:20] 作用：解析 JSON 文本；理由依据：取得结构化字段用于映射。
        decoded = json.loads(value)
    # [2026-07-04 10:18:20] 作用：捕获无效 JSON；理由依据：映射层不掩盖为模拟成功。
    except json.JSONDecodeError:
        # [2026-07-04 10:18:20] 作用：返回空列表；理由依据：上游原始字段仍保留用于排查。
        return []
    # [2026-07-04 10:18:20] 作用：兼容单字典结果；理由依据：只有一条知识时模型可能省略数组。
    if isinstance(decoded, dict):
        # [2026-07-04 10:18:20] 作用：包装单字典为列表；理由依据：统一后续循环接口。
        decoded = [decoded]
    # [2026-07-04 10:18:20] 作用：验证最终顶层类型；理由依据：非列表结构不能映射卡片。
    if not isinstance(decoded, list):
        # [2026-07-04 10:18:20] 作用：返回空列表；理由依据：避免错误类型进入 WebUI。
        return []
    # [2026-07-04 10:18:20] 作用：仅返回字典知识项；理由依据：保证字段访问安全。
    return [item for item in decoded if isinstance(item, dict)]

# [2026-07-04 10:18:20] 作用：声明总处理结果到 WebUI 合同的映射函数；理由依据：隔离业务响应与前端展示字段。
def map_process_result(result: dict[str, Any]) -> dict[str, Any]:
    # [2026-07-04 10:18:20] 作用：解析问答项；理由依据：生成问答知识卡片。
    qa_items = _parse_items(result.get("qa_analysis"))
    # [2026-07-04 10:18:20] 作用：解析意图项；理由依据：生成意图知识卡片。
    intent_items = _parse_items(result.get("intent_analysis"))
    # [2026-07-04 10:18:20] 作用：读取问答数据库 ID；理由依据：卡片主键与 AI_Wendajilu 保持一致。
    qa_ids = list(result.get("qa_pair_ids") or [])
    # [2026-07-04 10:18:20] 作用：读取意图数据库 ID；理由依据：卡片主键与 AI_Yitu 保持一致。
    intent_ids = list(result.get("intent_ids") or [])
    # [2026-07-04 10:18:20] 作用：初始化知识卡片列表；理由依据：按问答后意图顺序响应前端。
    knowledge_items: list[dict[str, Any]] = []
    # [2026-07-04 10:18:20] 作用：遍历问答提取项；理由依据：每个独立问题形成一张知识卡片。
    for index, item in enumerate(qa_items):
        # [2026-07-04 10:18:20] 作用：追加问答卡片；理由依据：标题、标注和正文分别对应标准问题、描述/场景和答案。
        knowledge_items.append({"id": qa_ids[index] if index < len(qa_ids) else f"qa-{index + 1}", "title": item.get("standard_question") or item.get("question") or "", "marker": item.get("description") or item.get("question_scene") or "", "body": item.get("answer") or "", "status": "pending", "kind": "qa"})
    # [2026-07-04 10:18:20] 作用：遍历意图提取项；理由依据：每个独立意图形成一张知识卡片。
    for index, item in enumerate(intent_items):
        # [2026-07-04 10:18:20] 作用：追加意图卡片；理由依据：标题、标注和正文分别对应 intent、evidence 和 description。
        knowledge_items.append({"id": intent_ids[index] if index < len(intent_ids) else f"intent-{index + 1}", "title": item.get("intent") or "", "marker": item.get("evidence") or "", "body": item.get("description") or "", "status": "pending", "kind": "intent"})
    # [2026-07-04 10:18:20] 作用：读取完整转录文本；理由依据：全文侧栏和摘要均必须来自真实语音解析。
    raw_text = str(result.get("raw_text") or "")
    # [2026-07-04 10:18:20] 作用：构造最终 WebUI 响应；理由依据：同时满足页面展示和数据库验收需要。
    return {
        # [2026-07-04 10:18:20] 作用：返回上传原文件名；理由依据：保持中文文件名称。
        "fileName": str(result.get("source_file_name") or result.get("file_name") or ""),
        # [2026-07-04 10:18:20] 作用：返回截断原文摘要；理由依据：列表预览不重复伪造模型摘要。
        "originalSummary": raw_text[:240],
        # [2026-07-04 10:18:20] 作用：返回完整转录文本；理由依据：前端需显示真实解析内容。
        "fullText": raw_text,
        # [2026-07-04 10:18:20] 作用：返回提示词分析块；理由依据：页面展示真实意图与问答提取数量和内容。
        "analysisBlocks": [{"id": "qaExtract", "title": "问答知识提取", "icon": "知识标注提示词小图标.png", "content": f"DeepSeek 提取问答 {len(qa_items)} 条"}, {"id": "intentExtract", "title": "意图发现AI提取", "icon": "意图发现AI提取小图标.png", "content": f"DeepSeek 提取意图 {len(intent_items)} 条"}],
        # [2026-07-04 10:18:20] 作用：返回全部真实知识卡片；理由依据：禁止后端失败时用模拟卡片替代。
        "knowledgeItems": knowledge_items,
        # [2026-07-04 10:18:20] 作用：返回原始数据 ID；理由依据：验收脚本据此查询 AI_YuanShishuju。
        "rawDataId": result.get("raw_data_id"),
        # [2026-07-04 10:18:20] 作用：返回问答 ID 列表；理由依据：验收脚本据此查询 AI_Wendajilu。
        "qaPairIds": qa_ids,
        # [2026-07-04 10:18:20] 作用：返回意图 ID 列表；理由依据：验收脚本据此查询 AI_Yitu。
        "intentIds": intent_ids,
        # [2026-07-04 10:18:20] 作用：返回解析引擎名称；理由依据：报告需证明实际语音解析路径。
        "engine": result.get("engine"),
    # [2026-07-04 10:18:20] 作用：结束 WebUI 响应字典；理由依据：形成稳定 JSON 合同。
    }
