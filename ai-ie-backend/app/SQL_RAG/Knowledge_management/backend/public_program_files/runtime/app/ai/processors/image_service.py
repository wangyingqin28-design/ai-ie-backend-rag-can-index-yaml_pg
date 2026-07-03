# [2026-07-03 18:11:51] 作用：导入依赖 `import base64`，供 模块级初始化 使用；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
import base64
# [2026-07-03 18:11:51] 作用：导入依赖 `import mimetypes`，供 模块级初始化 使用；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
import mimetypes
# [2026-07-03 18:11:51] 作用：导入依赖 `from app.config import Config`，供 模块级初始化 使用；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
from app.config import Config
# [2026-07-03 18:11:51] 作用：导入依赖 `from app.ai.prompts import OCR_PROMPT, IMAGE_PROMPT`，供 模块级初始化 使用；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
from app.ai.prompts import OCR_PROMPT, IMAGE_PROMPT
# [2026-07-03 18:11:51] 作用：导入依赖 `from app.ai.llm.llm_client import chat_complete`，供 模块级初始化 使用；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
from app.ai.llm.llm_client import chat_complete
# [2026-07-03 18:11:51] 作用：为 config 构造并保存赋值结果；本行执行 `config = Config()`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行属于模块级初始化
config = Config()
# [2026-07-03 18:11:51] 作用：声明同步函数 image_to_base64，封装可复用的处理步骤；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 image_to_base64
def image_to_base64(image_path: str) -> tuple[str, str]:
    # [2026-07-03 18:11:51] 作用：在 image_to_base64 中执行具体代码片段 `"""读取本地图片并转换成视觉模型可接收的 base64 data URL 数据。"""`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 image_to_base64
    """读取本地图片并转换成视觉模型可接收的 base64 data URL 数据。"""
    # [2026-07-03 18:11:51] 作用：为 (mime_type, _) 构造并保存赋值结果；本行执行 `mime_type, _ = mimetypes.guess_type(image_path)`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 image_to_base64
    mime_type, _ = mimetypes.guess_type(image_path)
    # [2026-07-03 18:11:51] 作用：在 image_to_base64 中按条件 `if not mime_type:` 选择执行分支；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 image_to_base64
    if not mime_type:
        # [2026-07-03 18:11:51] 作用：为 mime_type 构造并保存赋值结果；本行执行 `mime_type = "image/jpeg"`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 image_to_base64
        mime_type = "image/jpeg"
    # [2026-07-03 18:11:51] 作用：在 image_to_base64 中用 `with open(image_path, "rb") as f:` 管理资源生命周期；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 image_to_base64
    with open(image_path, "rb") as f:
        # [2026-07-03 18:11:51] 作用：为 image_base64 构造并保存赋值结果；本行执行 `image_base64 = base64.b64encode(f.read()).decode("utf-8")`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 image_to_base64
        image_base64 = base64.b64encode(f.read()).decode("utf-8")
    # [2026-07-03 18:11:51] 作用：从 image_to_base64 返回表达式 `return image_base64, mime_type` 的结果；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 image_to_base64
    return image_base64, mime_type
# [2026-07-03 18:11:51] 作用：声明同步函数 build_image_messages，封装可复用的处理步骤；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
def build_image_messages(image_base64: str, mime_type: str, prompt: str):
    # [2026-07-03 18:11:51] 作用：在 build_image_messages 中执行具体代码片段 `"""构造 OpenAI 兼容多模态 messages，包含文本 prompt 和图片内容。"""`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
    """构造 OpenAI 兼容多模态 messages，包含文本 prompt 和图片内容。"""
    # [2026-07-03 18:11:51] 作用：从 build_image_messages 返回表达式 `return [` 的结果；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
    return [
        # [2026-07-03 18:11:51] 作用：在 build_image_messages 中执行具体代码片段 `{`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
        {
            # [2026-07-03 18:11:51] 作用：完善 同步函数 build_image_messages 的签名或多行表达式片段 `"role": "user",`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
            "role": "user",
            # [2026-07-03 18:11:51] 作用：在 build_image_messages 中执行具体代码片段 `"content": [`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
            "content": [
                # [2026-07-03 18:11:51] 作用：完善 同步函数 build_image_messages 的签名或多行表达式片段 `{"type": "text", "text": prompt},`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
                {"type": "text", "text": prompt},
                # [2026-07-03 18:11:51] 作用：在 build_image_messages 中执行具体代码片段 `{`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
                {
                    # [2026-07-03 18:11:51] 作用：完善 同步函数 build_image_messages 的签名或多行表达式片段 `"type": "image_url",`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
                    "type": "image_url",
                    # [2026-07-03 18:11:51] 作用：在 build_image_messages 中执行具体代码片段 `"image_url": {`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
                    "image_url": {
                        # [2026-07-03 18:11:51] 作用：完善 同步函数 build_image_messages 的签名或多行表达式片段 `"url": f"data:{mime_type};base64,{image_base64}",`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
                        "url": f"data:{mime_type};base64,{image_base64}",
                    # [2026-07-03 18:11:51] 作用：完善 同步函数 build_image_messages 的签名或多行表达式片段 `},`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
                    },
                # [2026-07-03 18:11:51] 作用：完善 同步函数 build_image_messages 的签名或多行表达式片段 `},`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
                },
            # [2026-07-03 18:11:51] 作用：完善 同步函数 build_image_messages 的签名或多行表达式片段 `],`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
            ],
        # [2026-07-03 18:11:51] 作用：在 build_image_messages 中执行具体代码片段 `}`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
        }
    # [2026-07-03 18:11:51] 作用：在 build_image_messages 中执行具体代码片段 `]`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于同步函数 build_image_messages
    ]
# [2026-07-03 18:11:51] 作用：声明异步函数 call_vision_model，提供可等待的链路处理入口；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 call_vision_model
async def call_vision_model(image_path: str, prompt: str):
    # [2026-07-03 18:11:51] 作用：在 call_vision_model 中执行具体代码片段 `"""调用视觉模型；图片识别和图片 OCR 都复用这个底层方法。"""`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 call_vision_model
    """调用视觉模型；图片识别和图片 OCR 都复用这个底层方法。"""
    # [2026-07-03 18:11:51] 作用：为 (image_base64, mime_type) 构造并保存赋值结果；本行执行 `image_base64, mime_type = image_to_base64(image_path)`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 call_vision_model
    image_base64, mime_type = image_to_base64(image_path)
    # [2026-07-03 18:11:51] 作用：为 messages 构造并保存赋值结果；本行执行 `messages = build_image_messages(`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 call_vision_model
    messages = build_image_messages(
        # [2026-07-03 18:11:51] 作用：为 messages 构造并保存赋值结果；本行执行 `image_base64=image_base64,`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 call_vision_model
        image_base64=image_base64,
        # [2026-07-03 18:11:51] 作用：为 messages 构造并保存赋值结果；本行执行 `mime_type=mime_type,`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 call_vision_model
        mime_type=mime_type,
        # [2026-07-03 18:11:51] 作用：为 messages 构造并保存赋值结果；本行执行 `prompt=prompt,`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 call_vision_model
        prompt=prompt,
    # [2026-07-03 18:11:51] 作用：为 messages 构造并保存赋值结果；本行执行 `)`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 call_vision_model
    )
    # [2026-07-03 18:11:51] 作用：从 call_vision_model 返回表达式 `return await chat_complete(` 的结果；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 call_vision_model
    return await chat_complete(
        # [2026-07-03 18:11:51] 作用：完善 异步函数 call_vision_model 的签名或多行表达式片段 `model=config.VISION_MODEL,`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 call_vision_model
        model=config.VISION_MODEL,
        # [2026-07-03 18:11:51] 作用：完善 异步函数 call_vision_model 的签名或多行表达式片段 `messages=messages,`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 call_vision_model
        messages=messages,
    # [2026-07-03 18:11:51] 作用：完善 异步函数 call_vision_model 的签名或多行表达式片段 `)`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 call_vision_model
    )
# [2026-07-03 18:11:51] 作用：声明异步函数 recognize_image，提供可等待的链路处理入口；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 recognize_image
async def recognize_image(image_path: str):
    # [2026-07-03 18:11:51] 作用：在 recognize_image 中执行具体代码片段 `"""图片理解：描述图片中的对象、场景、关系和重要细节。"""`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 recognize_image
    """图片理解：描述图片中的对象、场景、关系和重要细节。"""
    # [2026-07-03 18:11:51] 作用：为 prompt 构造并保存赋值结果；本行执行 `prompt = IMAGE_PROMPT`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 recognize_image
    prompt = IMAGE_PROMPT
    # [2026-07-03 18:11:51] 作用：从 recognize_image 返回表达式 `return await call_vision_model(image_path, prompt)` 的结果；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 recognize_image
    return await call_vision_model(image_path, prompt)
# [2026-07-03 18:11:51] 作用：声明异步函数 ocr_image，提供可等待的链路处理入口；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 ocr_image
async def ocr_image(image_path: str):
    # [2026-07-03 18:11:51] 作用：在 ocr_image 中执行具体代码片段 `"""图片 OCR：只提取图片中的可见文字。"""`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 ocr_image
    """图片 OCR：只提取图片中的可见文字。"""
    # [2026-07-03 18:11:51] 作用：为 prompt 构造并保存赋值结果；本行执行 `prompt = OCR_PROMPT`；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 ocr_image
    prompt = OCR_PROMPT
    # [2026-07-03 18:11:51] 作用：从 ocr_image 返回表达式 `return await call_vision_model(image_path, prompt)` 的结果；理由依据：源模块 app.ai.processors.image_service 被两条执行链共同依赖，按去重方案归入公共程序层；本行位于异步函数 ocr_image
    return await call_vision_model(image_path, prompt)
