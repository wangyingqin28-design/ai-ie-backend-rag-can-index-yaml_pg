# [2026-07-04 10:18:20] 作用：导入路径工具定位端到端验收器；理由依据：契约测试必须读取实际将被操作人员执行的脚本。
from pathlib import Path


# [2026-07-04 10:18:20] 作用：定位 Knowledge_management 根目录；理由依据：测试文件与工具、报告使用固定项目内相对关系。
KNOWLEDGE_ROOT = Path(__file__).resolve().parents[1]
# [2026-07-04 10:18:20] 作用：定位待实现的真实音频验收脚本；理由依据：计划要求使用独立工具重复验证启动后的完整链路。
VERIFIER = KNOWLEDGE_ROOT / "tools" / "verify_full_stack_audio_ingestion.py"


# [2026-07-04 10:18:20] 作用：验证验收器包含真实代理上传、哈希和三表逐列核验能力；理由依据：只检查 HTTP 200 或返回 ID 不能证明字段正确入库。
def test_verifier_covers_real_upload_schema_and_rows() -> None:
    # [2026-07-04 10:18:20] 作用：断言验收脚本已经创建；理由依据：缺少独立验收器就无法复现本次真实测试。
    assert VERIFIER.is_file()
    # [2026-07-04 10:18:20] 作用：读取验收器完整源代码；理由依据：静态契约需检查关键安全和验证路径。
    source = VERIFIER.read_text(encoding="utf-8")
    # [2026-07-04 10:18:20] 作用：断言真实请求经过 18321 WebUI 同源代理；理由依据：不得绕过用户要求串联的前端服务。
    assert "http://127.0.0.1:18321/api/knowledge/parse" in source
    # [2026-07-04 10:18:20] 作用：断言验收器计算 SHA256；理由依据：报告必须证明被测文件确实是指定录音。
    assert "sha256" in source.lower()
    # [2026-07-04 10:18:20] 作用：断言验收器选择真实资产类型主键；理由依据：ZcLeiXin 不能写入虚构或错表字段。
    assert "AI_ZiChanLeiXing" in source and "zclxId" in source
    # [2026-07-04 10:18:20] 作用：断言三张目标表均被逐表查询；理由依据：原始数据、问答和意图任何一表都不能漏验。
    assert all(table in source for table in ("AI_YuanShishuju", "AI_Wendajilu", "AI_Yitu"))
    # [2026-07-04 10:18:20] 作用：断言验收器比较 ORM 和直播数据库列集合；理由依据：防止迁移代码漏掉真实表新增列。
    assert "orm_columns" in source and "database_columns" in source
    # [2026-07-04 10:18:20] 作用：断言验收器要求三类返回主键非空；理由依据：缺少任一 ID 都无法证明对应写库成功。
    assert all(name in source for name in ("rawDataId", "qaPairIds", "intentIds"))


# [2026-07-04 10:18:20] 作用：验证验收器只保留脱敏证据且绝不清理测试记录；理由依据：用户要求新入库内容可见并禁止把敏感连接信息写入报告。
def test_verifier_retains_rows_and_redacts_report() -> None:
    # [2026-07-04 10:18:20] 作用：读取验收器源代码用于安全契约断言；理由依据：删除 SQL 和敏感报告键可在真实调用前静态拦截。
    source = VERIFIER.read_text(encoding="utf-8")
    # [2026-07-04 10:18:20] 作用：禁止验收器包含删除三表记录的 SQL；理由依据：本次真实测试数据必须保留供 Navicat 核对。
    assert "delete from" not in source.lower()
    # [2026-07-04 10:18:20] 作用：断言脚本使用明确的脱敏报告字段白名单；理由依据：报告只能包含端口、模型名、ID、计数、长度、布尔值和文件哈希。
    assert "SAFE_REPORT_KEYS" in source
    # [2026-07-04 10:18:20] 作用：断言报告写入前执行敏感词检查；理由依据：API Key、密码或完整连接串不得落盘。
    assert "assert_report_is_redacted" in source
