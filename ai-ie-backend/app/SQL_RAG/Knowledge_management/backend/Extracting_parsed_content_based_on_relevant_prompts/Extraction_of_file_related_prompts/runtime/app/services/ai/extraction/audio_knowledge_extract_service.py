# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/services/ai/extraction/audio_knowledge_extract_service.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
import json
from typing import Any

from app.ai.llm.llm_client import llm_model_func
from app.ai.prompts import (
    QA_EXTRACTION_PROMPT,
    OUTPUT_FORMAT_PROMPT,
    DESCRIPTION_PROMPT,
    YT_PROMPT,
    AUDIO_QA_USER_PROMPT_TEMPLATE,
)
from app.services.ai.knowledge.qa_pair_service import parse_ai_qa_result
from app.services.ai.knowledge.intent_service import parse_ai_intent_result


async def extract_audio_qa(raw_text: str) -> str:
    """
    使用问答提取提示词，从原始文本中提取问答对。

    参数:
        raw_text: 文件、音频、图片或文档解析出来的原始文本。

    返回:
        AI 返回的原始字符串，一般应该是 JSON 数组字符串。

    说明:
        这里使用的是 QA_EXTRACTION_PROMPT 作为系统提示词，
        AUDIO_QA_USER_PROMPT_TEMPLATE 作为用户提示词模板。
    """
    user_prompt = AUDIO_QA_USER_PROMPT_TEMPLATE.format(raw_text=raw_text)

    system_prompt = "\n\n".join([
        QA_EXTRACTION_PROMPT,
        OUTPUT_FORMAT_PROMPT,
    ])

    return await llm_model_func(
        user_prompt,
        system_prompt=system_prompt,
    )


async def extract_qa_description(qa_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """
    基于已经提取出来的问答对，继续生成每条问答的语义描述。

    参数:
        qa_items: 问答提取结果，已经被解析成 Python list。

    返回:
        描述提取结果，格式仍然是 list[dict]。

    说明:
        这一步不是直接分析 raw_text，而是分析问答提取后的结果。
        也就是说，描述提示词依赖问答提示词的输出。
    """
    # 如果前一步没有提取到问答，就没有必要继续生成描述
    if not qa_items:
        return []

    # 把问答列表转成 JSON 字符串，作为描述提示词的输入
    user_prompt = json.dumps(qa_items, ensure_ascii=False, indent=2)

    # 调用大模型，要求模型基于问答内容生成 description
    result = await llm_model_func(
        user_prompt,
        system_prompt=DESCRIPTION_PROMPT,
    )

    # 复用问答解析方法，把 AI 返回的 JSON 字符串解析成 list[dict]
    return parse_ai_qa_result(result)


def merge_qa_description(
    qa_items: list[dict[str, Any]],
    description_items: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """
    将描述提取结果合并回原始问答结果。

    参数:
        qa_items:
            原始问答提取结果。

        description_items:
            描述提示词生成的结果。

    返回:
        合并 description 后的问答列表。

    合并规则:
        优先使用 standard_question 作为匹配 key。
        如果没有 standard_question，则使用 question。
    """
    # 用于快速查找某个问题对应的 description
    description_map = {}

    # 先把描述结果整理成字典:
    # {
    #   "标准问题或原问题": "description"
    # }
    for item in description_items:
        key = item.get("standard_question") or item.get("question")

        if key:
            description_map[str(key).strip()] = item.get("description")

    merged = []

    # 遍历原始问答，将匹配到的 description 填回去
    for item in qa_items:
        # 复制一份，避免直接修改原始 qa_items
        new_item = dict(item)

        # 使用 standard_question 或 question 作为匹配依据
        key = new_item.get("standard_question") or new_item.get("question")

        if key:
            description = description_map.get(str(key).strip())

            # 如果找到了对应描述，就写入当前问答对象
            if description:
                new_item["description"] = description

        merged.append(new_item)

    return merged


async def extract_audio_intent(raw_text: str) -> str:
    """
    使用意图提取提示词，从原始文本中提取用户意图。

    参数:
        raw_text: 文件解析出来的原始文本。

    返回:
        AI 返回的原始字符串，一般应该是 JSON 数组字符串。

    说明:
        意图提取直接基于 raw_text 执行，
        不依赖问答提取结果。
    """
    # 将原始文本填充到用户提示词模板中
    user_prompt = AUDIO_QA_USER_PROMPT_TEMPLATE.format(raw_text=raw_text)

    # 调用大模型，要求模型按照 YT_PROMPT 输出意图结构
    return await llm_model_func(
        user_prompt,
        system_prompt=YT_PROMPT,
    )


async def extract_audio_knowledge(raw_text: str) -> dict[str, Any]:
    """
    固定执行三套知识提取流程。

    执行顺序:
        1. 从 raw_text 中提取问答对。
        2. 基于问答对生成 description。
        3. 将 description 合并回问答对。
        4. 从 raw_text 中提取用户意图。

    参数:
        raw_text: 文件解析后的原始文本。

    返回:
        包含问答结果、描述结果、意图结果的字典。
    """
    # 第一步：问答提取，得到 AI 原始返回字符串
    qa_analysis = await extract_audio_qa(raw_text)
    print("QA 原始返回:", qa_analysis)
    # 第二步：将问答 JSON 字符串解析成 Python list
    qa_items = parse_ai_qa_result(qa_analysis)
    print("QA 解析结果:", qa_items)
    # 第三步：基于问答列表生成 description
    description_items = await extract_qa_description(qa_items)

    # 第四步：把 description 合并到问答结果中
    qa_with_description = merge_qa_description(
        qa_items=qa_items,
        description_items=description_items,
    )

    # 第五步：意图提取，得到 AI 原始返回字符串
    intent_analysis = await extract_audio_intent(raw_text)

    # 第六步：将意图 JSON 字符串解析成 Python list
    intent_items = parse_ai_intent_result(intent_analysis)

    # 返回完整结构，供 process_service.py 后续入库和接口响应使用
    return {
        # 带 description 的问答 JSON 字符串，方便导出或保存
        "qa_analysis": json.dumps(qa_with_description, ensure_ascii=False),

        # 带 description 的问答列表，方便后续保存到问答表
        "qa_items": qa_with_description,

        # 单独返回 description 结果，方便前端展示或排查
        "description_items": description_items,

        # AI 原始意图提取结果
        "intent_analysis": intent_analysis,

        # 解析后的意图列表，方便保存到意图表
        "intent_items": intent_items,
    }