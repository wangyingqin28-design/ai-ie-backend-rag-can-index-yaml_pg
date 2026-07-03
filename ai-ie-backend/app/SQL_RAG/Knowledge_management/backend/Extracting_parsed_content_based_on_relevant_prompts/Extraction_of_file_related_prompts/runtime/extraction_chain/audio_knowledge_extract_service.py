# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
import json
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
from typing import Any
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
from app.ai.llm.llm_client import llm_model_func
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
from app.ai.prompts import (
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
    QA_EXTRACTION_PROMPT,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
    OUTPUT_FORMAT_PROMPT,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
    DESCRIPTION_PROMPT,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
    YT_PROMPT,
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
    AUDIO_QA_USER_PROMPT_TEMPLATE,
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
)
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
from extraction_chain.qa_pair_service import parse_ai_qa_result
# [2026-07-03 16:33:01] 作用：导入本节点运行所需依赖；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
from extraction_chain.intent_service import parse_ai_intent_result
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
async def extract_audio_qa(raw_text: str) -> str:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
    '\n    使用问答提取提示词，从原始文本中提取问答对。\n\n    参数:\n        raw_text: 文件、音频、图片或文档解析出来的原始文本。\n\n    返回:\n        AI 返回的原始字符串，一般应该是 JSON 数组字符串。\n\n    说明:\n        这里使用的是 QA_EXTRACTION_PROMPT 作为系统提示词，\n        AUDIO_QA_USER_PROMPT_TEMPLATE 作为用户提示词模板。\n    '
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
    user_prompt = AUDIO_QA_USER_PROMPT_TEMPLATE.format(raw_text=raw_text)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
    system_prompt = "\n\n".join([
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
        QA_EXTRACTION_PROMPT,
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
        OUTPUT_FORMAT_PROMPT,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
    ])
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
    return await llm_model_func(
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
        user_prompt,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
        system_prompt=system_prompt,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_qa
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
async def extract_qa_description(qa_items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    '\n    基于已经提取出来的问答对，继续生成每条问答的语义描述。\n\n    参数:\n        qa_items: 问答提取结果，已经被解析成 Python list。\n\n    返回:\n        描述提取结果，格式仍然是 list[dict]。\n\n    说明:\n        这一步不是直接分析 raw_text，而是分析问答提取后的结果。\n        也就是说，描述提示词依赖问答提示词的输出。\n    '
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    # 如果前一步没有提取到问答，就没有必要继续生成描述
    # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    if not qa_items:
        # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
        return []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    # 把问答列表转成 JSON 字符串，作为描述提示词的输入
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    user_prompt = json.dumps(qa_items, ensure_ascii=False, indent=2)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    # 调用大模型，要求模型基于问答内容生成 description
    # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    result = await llm_model_func(
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
        user_prompt,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
        system_prompt=DESCRIPTION_PROMPT,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    # 复用问答解析方法，把 AI 返回的 JSON 字符串解析成 list[dict]
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_qa_description
    return parse_ai_qa_result(result)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可复用的同步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
def merge_qa_description(
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    qa_items: list[dict[str, Any]],
    # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    description_items: list[dict[str, Any]],
# [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
) -> list[dict[str, Any]]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    '\n    将描述提取结果合并回原始问答结果。\n\n    参数:\n        qa_items:\n            原始问答提取结果。\n\n        description_items:\n            描述提示词生成的结果。\n\n    返回:\n        合并 description 后的问答列表。\n\n    合并规则:\n        优先使用 standard_question 作为匹配 key。\n        如果没有 standard_question，则使用 question。\n    '
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    # 用于快速查找某个问题对应的 description
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    description_map = {}
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    # 先把描述结果整理成字典:
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    # {
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    #   "标准问题或原问题": "description"
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    # }
    # [2026-07-03 16:33:01] 作用：逐项处理集合或重复任务；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    for item in description_items:
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
        key = item.get("standard_question") or item.get("question")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
        if key:
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
            description_map[str(key).strip()] = item.get("description")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    merged = []
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    # 遍历原始问答，将匹配到的 description 填回去
    # [2026-07-03 16:33:01] 作用：逐项处理集合或重复任务；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    for item in qa_items:
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
        # 复制一份，避免直接修改原始 qa_items
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
        new_item = dict(item)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
        # 使用 standard_question 或 question 作为匹配依据
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
        key = new_item.get("standard_question") or new_item.get("question")
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
        # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
        if key:
            # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
            description = description_map.get(str(key).strip())
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
            # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
            # 如果找到了对应描述，就写入当前问答对象
            # [2026-07-03 16:33:01] 作用：依据当前状态选择执行分支；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
            if description:
                # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
                new_item["description"] = description
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
        # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
        merged.append(new_item)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于同步函数 merge_qa_description
    return merged
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_intent
async def extract_audio_intent(raw_text: str) -> str:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_intent
    '\n    使用意图提取提示词，从原始文本中提取用户意图。\n\n    参数:\n        raw_text: 文件解析出来的原始文本。\n\n    返回:\n        AI 返回的原始字符串，一般应该是 JSON 数组字符串。\n\n    说明:\n        意图提取直接基于 raw_text 执行，\n        不依赖问答提取结果。\n    '
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_intent
    # 将原始文本填充到用户提示词模板中
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_intent
    user_prompt = AUDIO_QA_USER_PROMPT_TEMPLATE.format(raw_text=raw_text)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_intent
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_intent
    # 调用大模型，要求模型按照 YT_PROMPT 输出意图结构
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_intent
    return await llm_model_func(
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_intent
        user_prompt,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_intent
        system_prompt=YT_PROMPT,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_intent
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于模块 extraction_chain.audio_knowledge_extract_service 的模块级声明
# [2026-07-03 16:33:01] 作用：定义可等待的异步处理节点；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
async def extract_audio_knowledge(raw_text: str) -> dict[str, Any]:
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    '\n    固定执行三套知识提取流程。\n\n    执行顺序:\n        1. 从 raw_text 中提取问答对。\n        2. 基于问答对生成 description。\n        3. 将 description 合并回问答对。\n        4. 从 raw_text 中提取用户意图。\n\n    参数:\n        raw_text: 文件解析后的原始文本。\n\n    返回:\n        包含问答结果、描述结果、意图结果的字典。\n    '
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    # 第一步：问答提取，得到 AI 原始返回字符串
    # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    qa_analysis = await extract_audio_qa(raw_text)
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    print("QA 原始返回:", qa_analysis)
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    # 第二步：将问答 JSON 字符串解析成 Python list
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    qa_items = parse_ai_qa_result(qa_analysis)
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    print("QA 解析结果:", qa_items)
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    # 第三步：基于问答列表生成 description
    # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    description_items = await extract_qa_description(qa_items)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    # 第四步：把 description 合并到问答结果中
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    qa_with_description = merge_qa_description(
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        qa_items=qa_items,
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        description_items=description_items,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    )
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    # 第五步：意图提取，得到 AI 原始返回字符串
    # [2026-07-03 16:33:01] 作用：等待异步下游完成并接收结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    intent_analysis = await extract_audio_intent(raw_text)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    # 第六步：将意图 JSON 字符串解析成 Python list
    # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    intent_items = parse_ai_intent_result(intent_analysis)
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    # 返回完整结构，供 process_service.py 后续入库和接口响应使用
    # [2026-07-03 16:33:01] 作用：向调用方返回本节点结果；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    return {
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        # 带 description 的问答 JSON 字符串，方便导出或保存
        # [2026-07-03 16:33:01] 作用：保存配置、参数或中间运行状态；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        "qa_analysis": json.dumps(qa_with_description, ensure_ascii=False),
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        # 带 description 的问答列表，方便后续保存到问答表
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        "qa_items": qa_with_description,
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        # 单独返回 description 结果，方便前端展示或排查
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        "description_items": description_items,
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        # AI 原始意图提取结果
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        "intent_analysis": intent_analysis,
# [2026-07-03 16:33:01] 作用：分隔相邻逻辑块；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        # [2026-07-03 16:33:01] 作用：保留原实现注释并说明约束；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        # 解析后的意图列表，方便保存到意图表
        # [2026-07-03 16:33:01] 作用：继续构造多行调用或数据结构；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
        "intent_items": intent_items,
    # [2026-07-03 16:33:01] 作用：执行当前节点的数据处理或控制表达式；理由依据：DeepSeek 提取入库业务链所有；本行属于异步函数 extract_audio_knowledge
    }
