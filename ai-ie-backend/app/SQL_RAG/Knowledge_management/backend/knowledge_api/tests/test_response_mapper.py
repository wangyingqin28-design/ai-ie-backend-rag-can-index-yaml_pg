# [2026-07-04 10:18:20] 作用：导入 JSON 序列化组件；理由依据：模拟 process_service 返回的问答与意图 JSON 字符串。
import json
# [2026-07-04 10:18:20] 作用：导入待实现响应映射函数；理由依据：先定义 WebUI 所需稳定返回合同。
from knowledge_api.response_mapper import map_process_result

# [2026-07-04 10:18:20] 作用：验证问答和意图都能映射为 WebUI 知识卡片；理由依据：前端必须展示真实 DeepSeek 结果和数据库 ID。
def test_map_process_result_preserves_text_ids_and_knowledge_semantics() -> None:
    # [2026-07-04 10:18:20] 作用：构造一条问答和一条意图的真实形状输入；理由依据：覆盖两张明细表的展示字段。
    result = {
        # [2026-07-04 10:18:20] 作用：声明处理成功；理由依据：映射器只处理成功结果。
        "success": True,
        # [2026-07-04 10:18:20] 作用：提供上传原文件名；理由依据：WebUI 文件标题必须保持中文名称。
        "source_file_name": "新录音 4.m4a",
        # [2026-07-04 10:18:20] 作用：提供真实转录全文；理由依据：前端全文侧栏不得使用模拟内容。
        "raw_text": "真实转录文本",
        # [2026-07-04 10:18:20] 作用：提供原始数据 ID；理由依据：前端和验收脚本需查询 AI_YuanShishuju。
        "raw_data_id": "raw-id",
        # [2026-07-04 10:18:20] 作用：提供问答主键列表；理由依据：问答卡片 ID 应与数据库一致。
        "qa_pair_ids": ["qa-id"],
        # [2026-07-04 10:18:20] 作用：提供意图主键列表；理由依据：意图卡片 ID 应与数据库一致。
        "intent_ids": ["intent-id"],
        # [2026-07-04 10:18:20] 作用：提供问答 JSON；理由依据：映射标准问题、场景、答案和描述。
        "qa_analysis": json.dumps([{"question": "原问题", "standard_question": "标准知识问题", "answer": "客服答案", "question_scene": "采购场景", "description": "检索描述"}], ensure_ascii=False),
        # [2026-07-04 10:18:20] 作用：提供意图 JSON；理由依据：映射意图名称、说明和证据。
        "intent_analysis": json.dumps([{"intent": "咨询操作", "description": "用户需要操作指导", "evidence": "怎么操作"}], ensure_ascii=False),
    # [2026-07-04 10:18:20] 作用：结束模拟处理结果；理由依据：形成与 process_service 一致的字典。
    }
    # [2026-07-04 10:18:20] 作用：执行待测响应映射；理由依据：验证 API 返回给 WebUI 的最终结构。
    mapped = map_process_result(result)
    # [2026-07-04 10:18:20] 作用：断言文件名保持不变；理由依据：不得丢失中文原文件名。
    assert mapped["fileName"] == "新录音 4.m4a"
    # [2026-07-04 10:18:20] 作用：断言全文来自真实转录；理由依据：禁止模拟解析成功。
    assert mapped["fullText"] == "真实转录文本"
    # [2026-07-04 10:18:20] 作用：断言原始数据 ID 被返回；理由依据：支持三表链路核验。
    assert mapped["rawDataId"] == "raw-id"
    # [2026-07-04 10:18:20] 作用：断言问答 ID 列表被返回；理由依据：支持 AI_Wendajilu 查询。
    assert mapped["qaPairIds"] == ["qa-id"]
    # [2026-07-04 10:18:20] 作用：断言意图 ID 列表被返回；理由依据：支持 AI_Yitu 查询。
    assert mapped["intentIds"] == ["intent-id"]
    # [2026-07-04 10:18:20] 作用：断言问答标题使用标准问题；理由依据：不能把原问题重复写入标准标题。
    assert mapped["knowledgeItems"][0]["title"] == "标准知识问题"
    # [2026-07-04 10:18:20] 作用：断言问答正文使用客服答案；理由依据：卡片正文不能误用场景或描述。
    assert mapped["knowledgeItems"][0]["body"] == "客服答案"
    # [2026-07-04 10:18:20] 作用：断言意图标题使用 intent；理由依据：保持 AI_YiTu 字段语义。
    assert mapped["knowledgeItems"][1]["title"] == "咨询操作"
