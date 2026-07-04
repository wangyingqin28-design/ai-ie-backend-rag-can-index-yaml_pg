# [2026-07-04 10:18:20] 作用：导入 JSON 序列化组件；理由依据：问答列表需作为第二轮提示词输入并返回给保存服务。
import json
# [2026-07-04 10:18:20] 作用：导入任意值类型；理由依据：DeepSeek 提取项是包含多类型字段的字典。
from typing import Any
# [2026-07-04 10:18:20] 作用：导入公共大模型调用函数；理由依据：问答、描述和意图三轮均必须走已配置的硅基流动兼容 API。
from app.ai.llm.llm_client import llm_model_func
# [2026-07-04 10:18:20] 作用：开始导入公共提示词常量；理由依据：提取链不重复复制公共提示词正文。
from app.ai.prompts import (
    # [2026-07-04 10:18:20] 作用：导入问答提取规则；理由依据：限定只依据音频原文提取。
    QA_EXTRACTION_PROMPT,
    # [2026-07-04 10:18:20] 作用：导入问答 JSON 输出格式；理由依据：约束 question、answer、scene、evidence 等字段。
    OUTPUT_FORMAT_PROMPT,
    # [2026-07-04 10:18:20] 作用：导入检索描述生成规则；理由依据：Biaozhu_true 必须来源于独立描述提示词。
    DESCRIPTION_PROMPT,
    # [2026-07-04 10:18:20] 作用：导入意图提取规则；理由依据：AI_Yitu 三个业务文本字段由该提示词生成。
    YT_PROMPT,
    # [2026-07-04 10:18:20] 作用：导入音频原文用户模板；理由依据：问答与意图均需接收同一完整转录。
    AUDIO_QA_USER_PROMPT_TEMPLATE,
# [2026-07-04 10:18:20] 作用：结束公共提示词导入列表；理由依据：保持模块依赖明确。
)
# [2026-07-04 10:18:20] 作用：导入问答 JSON 解析函数；理由依据：描述生成前必须取得结构化问答列表。
from extraction_chain.qa_pair_service import parse_ai_qa_result
# [2026-07-04 10:18:20] 作用：导入意图 JSON 解析函数；理由依据：接口需返回结构化意图列表。
from extraction_chain.intent_service import parse_ai_intent_result

# [2026-07-04 10:18:20] 作用：补充答案完整度 JSON 合同；理由依据：旧公共输出格式漏掉 ZhuangTai 的唯一模型来源。
ANSWER_COMPLETENESS_PROMPT = """
每个问答对象还必须包含以下字段：
"answer_completeness": "完整/部分完整/不完整/未明确"
完整表示原文已给出可执行或明确肯否答案；部分完整、不完整、未明确必须按原文判断，禁止补全。
"""

# [2026-07-04 10:18:20] 作用：声明音频问答提取步骤；理由依据：第一轮 DeepSeek 调用生成问答及证据字段。
async def extract_audio_qa(raw_text: str) -> str:
    # [2026-07-04 10:18:20] 作用：把完整转录填入用户提示词；理由依据：模型只能依据本次音频原文判断。
    user_prompt = AUDIO_QA_USER_PROMPT_TEMPLATE.format(raw_text=raw_text)
    # [2026-07-04 10:18:20] 作用：组合问答规则、原 JSON 格式和完整度合同；理由依据：确保 ZhuangTai 有明确且可解析的来源。
    system_prompt = "\n\n".join([QA_EXTRACTION_PROMPT, OUTPUT_FORMAT_PROMPT, ANSWER_COMPLETENESS_PROMPT])
    # [2026-07-04 10:18:20] 作用：调用已配置大模型并返回原始 JSON 字符串；理由依据：保存前仍需统一解析和校验。
    return await llm_model_func(user_prompt, system_prompt=system_prompt)

# [2026-07-04 10:18:20] 作用：声明问答检索描述生成步骤；理由依据：description 与答案、场景具有不同字段语义。
async def extract_qa_description(qa_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # [2026-07-04 10:18:20] 作用：检测没有问答项的情况；理由依据：空输入无需发起第二轮 API 请求。
    if not qa_items:
        # [2026-07-04 10:18:20] 作用：返回空描述列表；理由依据：保持问答与描述数量逻辑一致。
        return []
    # [2026-07-04 10:18:20] 作用：序列化问答项供描述模型读取；理由依据：保留中文和字段结构。
    user_prompt = json.dumps(qa_items, ensure_ascii=False, indent=2)
    # [2026-07-04 10:18:20] 作用：调用描述提示词；理由依据：检索描述不能混入答案步骤。
    result = await llm_model_func(user_prompt, system_prompt=DESCRIPTION_PROMPT)
    # [2026-07-04 10:18:20] 作用：解析描述 JSON 列表；理由依据：后续需按 standard_question 合并。
    return parse_ai_qa_result(result)

# [2026-07-04 10:18:20] 作用：声明问答与描述合并函数；理由依据：Biaozhu_true 入库前需把第二轮结果写回对应问答。
def merge_qa_description(
    # [2026-07-04 10:18:20] 作用：接收第一轮问答项；理由依据：这些项包含问题、答案、场景和证据。
    qa_items: list[dict[str, Any]],
    # [2026-07-04 10:18:20] 作用：接收第二轮描述项；理由依据：这些项包含标准问题与 description。
    description_items: list[dict[str, Any]],
# [2026-07-04 10:18:20] 作用：结束合并函数签名并声明返回问答列表；理由依据：保存服务消费合并后的统一结构。
) -> list[dict[str, Any]]:
    # [2026-07-04 10:18:20] 作用：初始化描述索引；理由依据：按问题键查找避免依赖模型返回顺序。
    description_map: dict[str, Any] = {}
    # [2026-07-04 10:18:20] 作用：遍历描述结果；理由依据：构建标准问题到描述的确定映射。
    for item in description_items:
        # [2026-07-04 10:18:20] 作用：优先选择标准问题作为匹配键；理由依据：标准问题是知识库稳定标题。
        key = item.get("standard_question") or item.get("question")
        # [2026-07-04 10:18:20] 作用：忽略没有问题键的描述；理由依据：无法可靠关联时不能错配到其他问答。
        if key:
            # [2026-07-04 10:18:20] 作用：保存标准化键与 description；理由依据：去除无意义首尾空白。
            description_map[str(key).strip()] = item.get("description")
    # [2026-07-04 10:18:20] 作用：初始化合并结果；理由依据：不直接修改第一轮原始对象。
    merged: list[dict[str, Any]] = []
    # [2026-07-04 10:18:20] 作用：逐条处理问答；理由依据：保持第一轮问答顺序和数量。
    for item in qa_items:
        # [2026-07-04 10:18:20] 作用：复制问答字典；理由依据：避免给调用方输入产生副作用。
        new_item = dict(item)
        # [2026-07-04 10:18:20] 作用：取得问答匹配键；理由依据：与描述索引使用相同优先级。
        key = new_item.get("standard_question") or new_item.get("question")
        # [2026-07-04 10:18:20] 作用：只对有问题键的项查找描述；理由依据：防止空键误关联。
        if key:
            # [2026-07-04 10:18:20] 作用：读取对应检索描述；理由依据：description 必须属于同一标准问题。
            description = description_map.get(str(key).strip())
            # [2026-07-04 10:18:20] 作用：检测是否生成有效描述；理由依据：不以空值覆盖问答。
            if description:
                # [2026-07-04 10:18:20] 作用：把检索描述写回问答；理由依据：save_qa_pairs 从该字段写入 Biaozhu_true。
                new_item["description"] = description
        # [2026-07-04 10:18:20] 作用：追加合并后的问答项；理由依据：保持每条原问答均可进入后续保存。
        merged.append(new_item)
    # [2026-07-04 10:18:20] 作用：返回合并问答列表；理由依据：供 JSON 序列化和数据库映射使用。
    return merged

# [2026-07-04 10:18:20] 作用：声明音频意图提取步骤；理由依据：第三轮 DeepSeek 独立生成意图、描述、证据和时间。
async def extract_audio_intent(raw_text: str) -> str:
    # [2026-07-04 10:18:20] 作用：把完整转录填入用户提示词；理由依据：意图判断只能依据本次音频原文。
    user_prompt = AUDIO_QA_USER_PROMPT_TEMPLATE.format(raw_text=raw_text)
    # [2026-07-04 10:18:20] 作用：调用意图提示词并返回原始 JSON；理由依据：保存前需经过统一解析。
    return await llm_model_func(user_prompt, system_prompt=YT_PROMPT)

# [2026-07-04 10:18:20] 作用：声明三轮音频知识提取总入口；理由依据：固定执行问答、描述、意图并形成可入库结构。
async def extract_audio_knowledge(raw_text: str) -> dict[str, Any]:
    # [2026-07-04 10:18:20] 作用：执行第一轮问答提取；理由依据：先生成描述所依赖的基础问答项。
    qa_analysis = await extract_audio_qa(raw_text)
    # [2026-07-04 10:18:20] 作用：解析第一轮问答结果；理由依据：第二轮描述输入需要结构化列表。
    qa_items = parse_ai_qa_result(qa_analysis)
    # [2026-07-04 10:18:20] 作用：执行第二轮检索描述生成；理由依据：Biaozhu_true 不能由场景字段代替。
    description_items = await extract_qa_description(qa_items)
    # [2026-07-04 10:18:20] 作用：把描述合并回对应问答；理由依据：问答保存服务读取统一对象。
    qa_with_description = merge_qa_description(qa_items, description_items)
    # [2026-07-04 10:18:20] 作用：执行第三轮意图提取；理由依据：意图表字段直接来源于完整转录。
    intent_analysis = await extract_audio_intent(raw_text)
    # [2026-07-04 10:18:20] 作用：解析第三轮意图结果；理由依据：接口展示和数量核验需要结构化列表。
    intent_items = parse_ai_intent_result(intent_analysis)
    # [2026-07-04 10:18:20] 作用：返回问答、描述和意图完整结果；理由依据：process_service 需分别入库并响应前端。
    return {
        # [2026-07-04 10:18:20] 作用：返回带 description 的问答 JSON；理由依据：save_qa_pairs 直接消费该字符串。
        "qa_analysis": json.dumps(qa_with_description, ensure_ascii=False),
        # [2026-07-04 10:18:20] 作用：返回结构化问答列表；理由依据：接口映射和调试无需再次解析。
        "qa_items": qa_with_description,
        # [2026-07-04 10:18:20] 作用：返回独立描述列表；理由依据：前端可显示第二轮提取结果。
        "description_items": description_items,
        # [2026-07-04 10:18:20] 作用：返回原始意图 JSON；理由依据：save_intents 直接消费该字符串。
        "intent_analysis": intent_analysis,
        # [2026-07-04 10:18:20] 作用：返回结构化意图列表；理由依据：接口映射和数量核验使用。
        "intent_items": intent_items,
    # [2026-07-04 10:18:20] 作用：结束提取结果字典；理由依据：形成稳定的总调度返回合同。
    }
