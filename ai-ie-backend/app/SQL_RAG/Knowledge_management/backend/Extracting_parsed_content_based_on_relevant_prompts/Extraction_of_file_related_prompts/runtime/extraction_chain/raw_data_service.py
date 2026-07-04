# [2026-07-04 10:18:20] 作用：导入当前时间生成器；理由依据：原始数据入库必须记录 in_time。
from datetime import datetime
# [2026-07-04 10:18:20] 作用：导入同步会话组件；理由依据：保存服务沿用原项目 SQLAlchemy 同步事务边界。
from sqlalchemy.orm import Session, sessionmaker
# [2026-07-04 10:18:20] 作用：导入公共 PostgreSQL 同步引擎；理由依据：两条链路共享唯一数据库配置。
from app.config import sync_engine
# [2026-07-04 10:18:20] 作用：导入原始数据 ORM；理由依据：本服务只负责 AI_YuanShishuju 入库。
from extraction_chain.erp_ai_models import ErpYuanShiShuJu
# [2026-07-04 10:18:20] 作用：导入 UUID7 ID 生成器；理由依据：原始数据 ID 同时作为两张明细表的关联键。
from extraction_chain.snowflake_generator import generate_uuid7_id

# [2026-07-04 10:18:20] 作用：保留原项目文本切片公共函数；理由依据：执行链定义完整性要求不能遗漏已有 def，保存逻辑不再用它制造复合主键冲突。
def split_text(text: str, chunk_size: int = 2000) -> list[str]:
    # [2026-07-04 10:18:20] 作用：处理空文本输入；理由依据：空内容不应生成伪分块。
    if not text:
        # [2026-07-04 10:18:20] 作用：返回空分块集合；理由依据：调用方可据此跳过无意义处理。
        return []
    # [2026-07-04 10:18:20] 作用：按给定长度生成文本分块；理由依据：保留原 def 的独立复用行为但不用于原始表写入。
    return [text[index:index + chunk_size] for index in range(0, len(text), chunk_size)]

# [2026-07-04 10:18:20] 作用：把统一文件类型转换为数据库来源码；理由依据：AI_YuanShishuju.LaiYuan 使用整数枚举。
def _file_type_to_source(file_type: str | None) -> int | None:
    # [2026-07-04 10:18:20] 作用：定义文件类型到来源码映射；理由依据：沿用原项目 document/text/audio/image 的 1/2/3/4 约定。
    mapping = {"document": 1, "text": 2, "audio": 3, "image": 4}
    # [2026-07-04 10:18:20] 作用：返回对应来源码或未知值；理由依据：不为未识别类型编造来源。
    return mapping.get(file_type or "")

# [2026-07-04 10:18:20] 作用：声明原始转录保存入口；理由依据：文件解析完成后必须先生成统一原文关联记录。
def save_raw_text(
    # [2026-07-04 10:18:20] 作用：强制后续参数以关键字传入；理由依据：避免多个 ID 和路径参数发生位置错位。
    *,
    # [2026-07-04 10:18:20] 作用：接收完整转录文本；理由依据：ShuJu 字段应保存硅基流动返回的完整内容。
    raw_text: str,
    # [2026-07-04 10:18:20] 作用：接收服务端处理路径；理由依据：WenJianDiZhi 用于追踪上传来源。
    source_file_path: str | None = None,
    # [2026-07-04 10:18:20] 作用：接收统一文件类型；理由依据：用于计算 LaiYuan。
    file_type: str | None = None,
    # [2026-07-04 10:18:20] 作用：接收上传原文件名；理由依据：WenJianName 必须保留 `新录音 4.m4a`。
    source_file_name: str | None = None,
    # [2026-07-04 10:18:20] 作用：接收客户关联 ID；理由依据：该值参与原始表复合主键。
    guan_lian_ke_hu: int | str = 0,
    # [2026-07-04 10:18:20] 作用：接收企业 ID；理由依据：当前无企业上下文时允许为空。
    enterprise_id: int | str | None = None,
    # [2026-07-04 10:18:20] 作用：接收录入用户 ID；理由依据：当前无登录上下文时允许为空。
    in_userid: int | str | None = None,
    # [2026-07-04 10:18:20] 作用：接收资产类型 ID；理由依据：ZcLeiXin 必须关联真实资产类型。
    asset_type_id: str | None = None,
# [2026-07-04 10:18:20] 作用：结束保存入口签名并声明返回原文 ID；理由依据：下游问答与意图需要该 ID。
) -> str | None:
    # [2026-07-04 10:18:20] 作用：拒绝空白原文；理由依据：空转录不能生成知识明细的有效来源。
    if not raw_text or not raw_text.strip():
        # [2026-07-04 10:18:20] 作用：返回未生成标识；理由依据：调用方据此停止错误关联。
        return None
    # [2026-07-04 10:18:20] 作用：为本次完整原文生成 UUID7；理由依据：保证三表链路使用同一稳定关联键。
    raw_id = generate_uuid7_id()
    # [2026-07-04 10:18:20] 作用：创建同步会话工厂；理由依据：保持原项目事务提交和回滚语义。
    SessionLocal = sessionmaker(
        # [2026-07-04 10:18:20] 作用：绑定公共同步数据库引擎；理由依据：目标库连接由公共配置唯一提供。
        bind=sync_engine,
        # [2026-07-04 10:18:20] 作用：指定 SQLAlchemy Session 类型；理由依据：便于测试替换并保持同步 API。
        class_=Session,
        # [2026-07-04 10:18:20] 作用：提交后保留对象属性；理由依据：返回和测试阶段无需重新加载记录。
        expire_on_commit=False,
    # [2026-07-04 10:18:20] 作用：结束会话工厂配置；理由依据：形成可调用的 SessionLocal。
    )
    # [2026-07-04 10:18:20] 作用：自动管理数据库会话生命周期；理由依据：成功或失败均应关闭连接。
    with SessionLocal() as db:
        # [2026-07-04 10:18:20] 作用：开始原始数据事务保护；理由依据：失败时必须完整回滚。
        try:
            # [2026-07-04 10:18:20] 作用：构造单条完整原始数据记录；理由依据：TEXT 列可容纳全文且避免分块复合主键冲突。
            record = ErpYuanShiShuJu(
                # [2026-07-04 10:18:20] 作用：写入本次原始数据 UUID7；理由依据：作为两张明细表的 Yssj_id。
                shuju_id=raw_id,
                # [2026-07-04 10:18:20] 作用：写入资产类型 ID；理由依据：来源为上传表单且不得改写。
                ZcLeiXin=asset_type_id,
                # [2026-07-04 10:18:20] 作用：写入完整转录文本；理由依据：不能遗漏 2000 字后的内容。
                ShuJu=raw_text,
                # [2026-07-04 10:18:20] 作用：写入服务端处理路径；理由依据：沿用原项目来源字段语义。
                WenJianDiZhi=source_file_path,
                # [2026-07-04 10:18:20] 作用：写入上传原文件名；理由依据：便于 Navicat 按文件核验。
                WenJianName=source_file_name,
                # [2026-07-04 10:18:20] 作用：写入来源类型码；理由依据：audio 必须得到 3。
                LaiYuan=_file_type_to_source(file_type),
                # [2026-07-04 10:18:20] 作用：按真实 varchar 类型写入客户 ID；理由依据：避免 ORM 隐式整数类型错配。
                GuanLianKeHu=str(guan_lian_ke_hu),
                # [2026-07-04 10:18:20] 作用：按有无企业上下文写入企业 ID；理由依据：无上下文时正确值为 NULL。
                gs_id=None if enterprise_id is None else str(enterprise_id),
                # [2026-07-04 10:18:20] 作用：标记新记录未删除；理由依据：有效知识来源的 del_flag 必须为 false。
                del_flag=False,
                # [2026-07-04 10:18:20] 作用：显式保存未删除时间；理由依据：删除事件尚未发生时必须为 NULL。
                del_time=None,
                # [2026-07-04 10:18:20] 作用：按有无登录上下文写入录入人；理由依据：无用户时不能编造 ID。
                in_userid=None if in_userid is None else str(in_userid),
                # [2026-07-04 10:18:20] 作用：写入当前录入时间；理由依据：用于验收新增时间窗口。
                in_time=datetime.now(),
                # [2026-07-04 10:18:20] 作用：显式保存未修改人；理由依据：新增记录尚未发生修改。
                up_userid=None,
                # [2026-07-04 10:18:20] 作用：显式保存未修改时间；理由依据：新增记录尚未发生修改。
                up_time=None,
                # [2026-07-04 10:18:20] 作用：显式保存保留列为空；理由依据：原项目和目标库现存知识行均无 yima 业务赋值。
                yima=None,
            # [2026-07-04 10:18:20] 作用：结束原始记录构造；理由依据：形成完整 ORM 实例。
            )
            # [2026-07-04 10:18:20] 作用：把原始记录加入事务；理由依据：等待统一提交。
            db.add(record)
            # [2026-07-04 10:18:20] 作用：提交原始数据事务；理由依据：成功后问答和意图才能引用该 ID。
            db.commit()
            # [2026-07-04 10:18:20] 作用：返回原始数据 ID；理由依据：下游两张表使用它作为 Yssj_id。
            return raw_id
        # [2026-07-04 10:18:20] 作用：捕获任意入库异常；理由依据：禁止留下半提交事务。
        except Exception:
            # [2026-07-04 10:18:20] 作用：回滚失败事务；理由依据：维护原始表一致性。
            db.rollback()
            # [2026-07-04 10:18:20] 作用：向上重新抛出异常；理由依据：API 必须明确报告真实数据库失败。
            raise
