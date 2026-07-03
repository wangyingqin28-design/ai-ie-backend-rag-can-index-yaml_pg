# [2026-07-03 18:11:51] 作用：导入依赖 `from typing import Any`，供 模块级初始化 使用；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
from typing import Any
# [2026-07-03 18:11:51] 作用：导入依赖 `from openai import AsyncOpenAI`，供 模块级初始化 使用；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
from openai import AsyncOpenAI
# [2026-07-03 18:11:51] 作用：导入依赖 `from app.config import Config`，供 模块级初始化 使用；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
from app.config import Config
# [2026-07-03 18:11:51] 作用：为 config 构造并保存赋值结果；本行执行 `config = Config()`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
config = Config()
# [2026-07-03 18:11:51] 作用：声明同步函数 build_openai_client，封装可复用的处理步骤；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_openai_client
def build_openai_client() -> AsyncOpenAI:
    # [2026-07-03 18:11:51] 作用：在 build_openai_client 中执行具体代码片段 `"""创建异步 OpenAI 兼容客户端，当前配置指向外部模型服务。"""`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_openai_client
    """创建异步 OpenAI 兼容客户端，当前配置指向外部模型服务。"""
    # [2026-07-03 18:11:51] 作用：从 build_openai_client 返回表达式 `return AsyncOpenAI(` 的结果；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_openai_client
    return AsyncOpenAI(
        # [2026-07-03 18:11:51] 作用：完善 同步函数 build_openai_client 的签名或多行表达式片段 `api_key=config.embedding_service_api_key,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_openai_client
        api_key=config.embedding_service_api_key,
        # [2026-07-03 18:11:51] 作用：完善 同步函数 build_openai_client 的签名或多行表达式片段 `base_url=config.embedding_service_url,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_openai_client
        base_url=config.embedding_service_url,
    # [2026-07-03 18:11:51] 作用：完善 同步函数 build_openai_client 的签名或多行表达式片段 `)`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_openai_client
    )
# [2026-07-03 18:11:51] 作用：声明异步函数 chat_complete，提供可等待的链路处理入口；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
async def chat_complete(
    # [2026-07-03 18:11:51] 作用：完善 异步函数 chat_complete 的签名或多行表达式片段 `model: str,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
    model: str,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 chat_complete 的签名或多行表达式片段 `messages: list[dict[str, Any]],`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
    messages: list[dict[str, Any]],
    # [2026-07-03 18:11:51] 作用：完善 异步函数 chat_complete 的签名或多行表达式片段 `**kwargs,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
    **kwargs,
# [2026-07-03 18:11:51] 作用：在 chat_complete 中执行具体代码片段 `) -> str:`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
) -> str:
    # [2026-07-03 18:11:51] 作用：在 chat_complete 中执行具体代码片段 `"""通用聊天补全方法，文本模型和视觉模型最终都会走这里。"""`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
    """通用聊天补全方法，文本模型和视觉模型最终都会走这里。"""
    # [2026-07-03 18:11:51] 作用：为 client 构造并保存赋值结果；本行执行 `client = build_openai_client()`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
    client = build_openai_client()
    # [2026-07-03 18:11:51] 作用：为 response 构造并保存赋值结果；本行执行 `response = await client.chat.completions.create(`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
    response = await client.chat.completions.create(
        # [2026-07-03 18:11:51] 作用：为 response 构造并保存赋值结果；本行执行 `model=model,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
        model=model,
        # [2026-07-03 18:11:51] 作用：为 response 构造并保存赋值结果；本行执行 `messages=messages,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
        messages=messages,
        # [2026-07-03 18:11:51] 作用：为 response 构造并保存赋值结果；本行执行 `**kwargs,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
        **kwargs,
    # [2026-07-03 18:11:51] 作用：为 response 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
    )
    # [2026-07-03 18:11:51] 作用：从 chat_complete 返回表达式 `return response.choices[0].message.content or ""` 的结果；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 chat_complete
    return response.choices[0].message.content or ""
# [2026-07-03 18:11:51] 作用：声明异步函数 llm_model_func，提供可等待的链路处理入口；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
async def llm_model_func(
    # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `prompt,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    prompt,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `system_prompt=None,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    system_prompt=None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `history_messages=None,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    history_messages=None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `**kwargs,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    **kwargs,
# [2026-07-03 18:11:51] 作用：在 llm_model_func 中执行具体代码片段 `):`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
):
    # [2026-07-03 18:11:51] 作用：在 llm_model_func 中执行具体代码片段 `"""普通文本大模型调用，供文本摘要、兜底回答等场景使用。"""`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    """普通文本大模型调用，供文本摘要、兜底回答等场景使用。"""
    # [2026-07-03 18:11:51] 作用：为 history_messages 构造并保存赋值结果；本行执行 `history_messages = history_messages or []`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    history_messages = history_messages or []
    # [2026-07-03 18:11:51] 作用：为 messages 构造并保存赋值结果；本行执行 `messages = []`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    messages = []
    # [2026-07-03 18:11:51] 作用：在 llm_model_func 中按条件 `if system_prompt:` 选择执行分支；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    if system_prompt:
        # [2026-07-03 18:11:51] 作用：在 llm_model_func 中执行具体代码片段 `messages.append({`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
        messages.append({
            # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `"role": "system",`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
            "role": "system",
            # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `"content": system_prompt,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
            "content": system_prompt,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `})`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
        })
    # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `messages.extend(history_messages)`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    messages.extend(history_messages)
    # [2026-07-03 18:11:51] 作用：在 llm_model_func 中执行具体代码片段 `messages.append({`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    messages.append({
        # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `"role": "user",`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
        "role": "user",
        # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `"content": prompt,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
        "content": prompt,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `})`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    })
    # [2026-07-03 18:11:51] 作用：从 llm_model_func 返回表达式 `return await chat_complete(` 的结果；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    return await chat_complete(
        # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `model=config.LLM_MODEL,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
        model=config.LLM_MODEL,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `messages=messages,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
        messages=messages,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `**kwargs,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
        **kwargs,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 llm_model_func 的签名或多行表达式片段 `)`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 llm_model_func
    )
# [2026-07-03 18:11:51] 作用：声明异步函数 vision_model_func，提供可等待的链路处理入口；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
async def vision_model_func(
    # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `prompt,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
    prompt,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `system_prompt=None,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
    system_prompt=None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `history_messages=None,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
    history_messages=None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `image_data=None,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
    image_data=None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `messages=None,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
    messages=None,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `**kwargs,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
    **kwargs,
# [2026-07-03 18:11:51] 作用：在 vision_model_func 中执行具体代码片段 `):`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
):
    # [2026-07-03 18:11:51] 作用：在 vision_model_func 中执行具体代码片段 `"""视觉模型调用，兼容直接传 messages 或传单张 base64 图片两种形式。"""`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
    """视觉模型调用，兼容直接传 messages 或传单张 base64 图片两种形式。"""
    # [2026-07-03 18:11:51] 作用：在 vision_model_func 中按条件 `if messages:` 选择执行分支；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
    if messages:
        # [2026-07-03 18:11:51] 作用：从 vision_model_func 返回表达式 `return await chat_complete(` 的结果；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
        return await chat_complete(
            # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `model=config.VISION_MODEL,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
            model=config.VISION_MODEL,
            # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `messages=messages,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
            messages=messages,
            # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `**kwargs,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
            **kwargs,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `)`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
        )
    # [2026-07-03 18:11:51] 作用：在 vision_model_func 中按条件 `if image_data:` 选择执行分支；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
    if image_data:
        # [2026-07-03 18:11:51] 作用：为 message_list 构造并保存赋值结果；本行执行 `message_list = []`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
        message_list = []
        # [2026-07-03 18:11:51] 作用：在 vision_model_func 中按条件 `if system_prompt:` 选择执行分支；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
        if system_prompt:
            # [2026-07-03 18:11:51] 作用：在 vision_model_func 中执行具体代码片段 `message_list.append({`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
            message_list.append({
                # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `"role": "system",`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
                "role": "system",
                # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `"content": system_prompt,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
                "content": system_prompt,
            # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `})`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
            })
        # [2026-07-03 18:11:51] 作用：在 vision_model_func 中执行具体代码片段 `message_list.append({`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
        message_list.append({
            # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `"role": "user",`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
            "role": "user",
            # [2026-07-03 18:11:51] 作用：在 vision_model_func 中执行具体代码片段 `"content": [`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
            "content": [
                # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `{"type": "text", "text": prompt},`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
                {"type": "text", "text": prompt},
                # [2026-07-03 18:11:51] 作用：在 vision_model_func 中执行具体代码片段 `{`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
                {
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `"type": "image_url",`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
                    "type": "image_url",
                    # [2026-07-03 18:11:51] 作用：在 vision_model_func 中执行具体代码片段 `"image_url": {`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
                    "image_url": {
                        # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `"url": f"data:image/jpeg;base64,{image_data}",`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
                        "url": f"data:image/jpeg;base64,{image_data}",
                    # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `},`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
                    },
                # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `},`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
                },
            # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `],`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
            ],
        # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `})`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
        })
        # [2026-07-03 18:11:51] 作用：从 vision_model_func 返回表达式 `return await chat_complete(` 的结果；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
        return await chat_complete(
            # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `model=config.VISION_MODEL,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
            model=config.VISION_MODEL,
            # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `messages=message_list,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
            messages=message_list,
            # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `**kwargs,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
            **kwargs,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `)`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
        )
    # [2026-07-03 18:11:51] 作用：从 vision_model_func 返回表达式 `return await llm_model_func(` 的结果；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
    return await llm_model_func(
        # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `prompt,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
        prompt,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `system_prompt=system_prompt,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
        system_prompt=system_prompt,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `history_messages=history_messages,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
        history_messages=history_messages,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `**kwargs,`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
        **kwargs,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 vision_model_func 的签名或多行表达式片段 `)`；理由依据：源模块 app.ai.llm.llm_client 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 vision_model_func
    )
