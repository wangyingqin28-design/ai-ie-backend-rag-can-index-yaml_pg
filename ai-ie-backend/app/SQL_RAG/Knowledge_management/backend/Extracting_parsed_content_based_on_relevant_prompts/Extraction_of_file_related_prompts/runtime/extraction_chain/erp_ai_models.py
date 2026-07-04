# [2026-07-04 10:18:20] 作用：导入可空类型以声明数据库可空列；理由依据：三张目标表包含多项允许 NULL 的审核与审计字段。
from typing import Optional
# [2026-07-04 10:18:20] 作用：导入日期时间类型以标注时间戳列；理由依据：入库、审核、删除和更新时间均使用 PostgreSQL timestamp。
import datetime
# [2026-07-04 10:18:20] 作用：开始导入 SQLAlchemy 列类型与约束；理由依据：ORM 必须与实际 PostgreSQL 元数据逐列一致。
from sqlalchemy import (
    # [2026-07-04 10:18:20] 作用：导入布尔列类型；理由依据：原始数据有效标志 del_flag 为 boolean。
    Boolean,
    # [2026-07-04 10:18:20] 作用：导入时间戳列类型；理由依据：审计字段和状态时间为 timestamp。
    DateTime,
    # [2026-07-04 10:18:20] 作用：导入整数列类型；理由依据：来源类型与状态码为 integer。
    Integer,
    # [2026-07-04 10:18:20] 作用：导入复合主键约束；理由依据：三张业务表均使用数据库现有复合主键。
    PrimaryKeyConstraint,
    # [2026-07-04 10:18:20] 作用：导入字符串列类型；理由依据：ID、时间区间和保留列均为 varchar。
    String,
    # [2026-07-04 10:18:20] 作用：导入长文本列类型；理由依据：转录全文、问题、答案和描述均为 text。
    Text,
    # [2026-07-04 10:18:20] 作用：导入 SQL 默认表达式构造器；理由依据：del_flag 需要数据库 false 默认值。
    text,
# [2026-07-04 10:18:20] 作用：结束 SQLAlchemy 导入列表；理由依据：保持依赖边界清晰并通过 Python 语法解析。
)
# [2026-07-04 10:18:20] 作用：导入 SQLAlchemy 2 声明式映射类型；理由依据：三个 ORM 类使用 Mapped 与 mapped_column。
from sqlalchemy.orm import Mapped, mapped_column
# [2026-07-04 10:18:20] 作用：导入提取链独立声明基类；理由依据：业务专属 ORM 不应复制公共运行时的基类定义。
from extraction_chain.model_base import Base

# [2026-07-04 10:18:20] 作用：声明问答知识 ORM；理由依据：DeepSeek 问答结果必须完整映射到 AI_Wendajilu。
class ErpWendaJilu(Base):
    # [2026-07-04 10:18:20] 作用：指定问答表的精确大小写名称；理由依据：PostgreSQL 使用带引号的混合大小写表名。
    __tablename__ = "AI_Wendajilu"
    # [2026-07-04 10:18:20] 作用：开始配置问答表复合主键；理由依据：实际表由 wdjl_ id 与 Yssj_id 联合唯一。
    __table_args__ = (
        # [2026-07-04 10:18:20] 作用：保留数据库中包含空格的主键列名；理由依据：不能把 `wdjl_ id` 错写为 `wdjl_id`。
        PrimaryKeyConstraint("wdjl_ id", "Yssj_id", name="pk_AI_Wendajilu"),
    # [2026-07-04 10:18:20] 作用：结束问答表约束配置；理由依据：形成合法的 SQLAlchemy 表级参数元组。
    )
    # [2026-07-04 10:18:20] 作用：映射问答记录 UUID7；理由依据：每条问答需要独立且非自增的 varchar(64) 标识。
    wdjl_id: Mapped[str] = mapped_column("wdjl_ id", String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-04 10:18:20] 作用：映射原始数据关联 ID；理由依据：问答必须通过 Yssj_id 关联本次转录原文。
    Yssj_id: Mapped[str] = mapped_column("Yssj_id", String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-04 10:18:20] 作用：保存 DeepSeek 提取的客户原问题；理由依据：字段真值表规定来源为 question。
    AI_WenTi: Mapped[Optional[str]] = mapped_column("AI_WenTi", Text)
    # [2026-07-04 10:18:20] 作用：保存 DeepSeek 提取的客服答案；理由依据：字段真值表规定来源为 answer。
    AI_DaAn: Mapped[Optional[str]] = mapped_column("AI_DaAn", Text)
    # [2026-07-04 10:18:20] 作用：保存问题发生场景；理由依据：AI_Biaozhu 必须对应 question_scene 而非检索描述。
    AI_Biaozhu: Mapped[Optional[str]] = mapped_column("AI_Biaozhu", Text)
    # [2026-07-04 10:18:20] 作用：保存支撑问题判断的客户原文；理由依据：来源为 evidence.customer_text。
    WenTiYuanWen: Mapped[Optional[str]] = mapped_column("WenTiYuanWen", Text)
    # [2026-07-04 10:18:20] 作用：保存支撑答案判断的客服原文；理由依据：来源为 evidence.service_text。
    DaAnYuanWen: Mapped[Optional[str]] = mapped_column("DaAnYuanWen", Text)
    # [2026-07-04 10:18:20] 作用：保存标准化知识问题；理由依据：来源必须是 standard_question，不能重复写 question。
    WenTi_true: Mapped[Optional[str]] = mapped_column("WenTi_true", Text)
    # [2026-07-04 10:18:20] 作用：保存当前确认答案；理由依据：未人工校订前与 DeepSeek answer 保持一致。
    DaAn_true: Mapped[Optional[str]] = mapped_column("DaAn_true", Text)
    # [2026-07-04 10:18:20] 作用：保存检索语义描述；理由依据：来源为第二轮描述提示词的 description。
    Biaozhu_true: Mapped[Optional[str]] = mapped_column("Biaozhu_true", Text)
    # [2026-07-04 10:18:20] 作用：保存答案完整度状态码；理由依据：完整度映射为 1/2/3/4。
    ZhuangTai: Mapped[Optional[int]] = mapped_column("ZhuangTai", Integer)
    # [2026-07-04 10:18:20] 作用：保存未来审核人 ID；理由依据：实际列类型为 varchar(64)，新提取时为空。
    ZhuangTai_id: Mapped[Optional[str]] = mapped_column("ZhuangTai_id", String(64))
    # [2026-07-04 10:18:20] 作用：保存未来审核时间；理由依据：新提取记录尚未审核时为空。
    ZhuangTai_time: Mapped[Optional[datetime.datetime]] = mapped_column("ZhuangTai_time", DateTime)
    # [2026-07-04 10:18:20] 作用：保存问答对应的音频时间区间；理由依据：模型输出为区间字符串且实际列为 varchar(64)。
    YinPinShiJian: Mapped[Optional[str]] = mapped_column("YinPinShiJian", String(64))
    # [2026-07-04 10:18:20] 作用：保存企业 ID；理由依据：独立 WebUI 当前无企业上下文时允许为空。
    gsId: Mapped[Optional[str]] = mapped_column("gsId", String(64))
    # [2026-07-04 10:18:20] 作用：保存录入用户 ID；理由依据：独立 WebUI 当前无登录用户时允许为空。
    in_userid: Mapped[Optional[str]] = mapped_column("in_userid", String(64))
    # [2026-07-04 10:18:20] 作用：保存问答入库时间；理由依据：验收需按本次测试时间窗口定位新增记录。
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column("in_time", DateTime)
    # [2026-07-04 10:18:20] 作用：映射数据库保留列 yima；理由依据：实际表含该列且现有原项目逻辑统一保留为空。
    yima: Mapped[Optional[str]] = mapped_column("yima", String(64))

# [2026-07-04 10:18:20] 作用：声明意图知识 ORM；理由依据：DeepSeek 意图结果必须完整映射到 AI_Yitu。
class ErpYitu(Base):
    # [2026-07-04 10:18:20] 作用：指定意图表精确名称；理由依据：PostgreSQL 使用带引号的混合大小写表名。
    __tablename__ = "AI_Yitu"
    # [2026-07-04 10:18:20] 作用：开始配置意图表复合主键；理由依据：实际表由 yt_ id 与 Yssj_id 联合唯一。
    __table_args__ = (
        # [2026-07-04 10:18:20] 作用：保留数据库中包含空格的意图主键列名；理由依据：必须与真实表元数据一致。
        PrimaryKeyConstraint("yt_ id", "Yssj_id", name="pk_AI_Yitu"),
    # [2026-07-04 10:18:20] 作用：结束意图表约束配置；理由依据：形成合法的表级参数元组。
    )
    # [2026-07-04 10:18:20] 作用：映射意图 UUID7；理由依据：每条意图需要独立且非自增的 varchar(64) 标识。
    yt_id: Mapped[str] = mapped_column("yt_ id", String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-04 10:18:20] 作用：映射原始数据关联 ID；理由依据：意图必须关联本次转录原文。
    Yssj_id: Mapped[str] = mapped_column("Yssj_id", String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-04 10:18:20] 作用：保存简洁意图名称；理由依据：来源为 DeepSeek intent。
    AI_YiTu: Mapped[Optional[str]] = mapped_column("AI_YiTu", Text)
    # [2026-07-04 10:18:20] 作用：保存意图语义说明；理由依据：来源为 DeepSeek description。
    YiTu: Mapped[Optional[str]] = mapped_column("YiTu", Text)
    # [2026-07-04 10:18:20] 作用：保存意图证据原文；理由依据：来源为 DeepSeek evidence。
    BiaoZhu: Mapped[Optional[str]] = mapped_column("BiaoZhu", Text)
    # [2026-07-04 10:18:20] 作用：保存意图初始状态；理由依据：新提取记录固定为 0 待审核。
    ZhuangTai: Mapped[Optional[int]] = mapped_column("ZhuangTai", Integer)
    # [2026-07-04 10:18:20] 作用：保存未来审核人 ID；理由依据：实际列为 varchar(64)，新记录尚未审核。
    ZhuangTai_id: Mapped[Optional[str]] = mapped_column("ZhuangTai_id", String(64))
    # [2026-07-04 10:18:20] 作用：保存未来审核时间；理由依据：新提取记录尚未审核时为空。
    ZhuangTai_time: Mapped[Optional[datetime.datetime]] = mapped_column("ZhuangTai_time", DateTime)
    # [2026-07-04 10:18:20] 作用：保存意图对应音频时间区间；理由依据：DeepSeek time 对应实际 varchar(255) 列。
    ShiJian: Mapped[Optional[str]] = mapped_column("ShiJian", String(255))
    # [2026-07-04 10:18:20] 作用：保存企业 ID；理由依据：独立 WebUI 当前无企业上下文时允许为空。
    gsId: Mapped[Optional[str]] = mapped_column("gsId", String(64))
    # [2026-07-04 10:18:20] 作用：保存删除时间；理由依据：新增有效记录尚未删除时为空。
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column("del_time", DateTime)
    # [2026-07-04 10:18:20] 作用：保存录入用户 ID；理由依据：独立 WebUI 当前无登录用户时允许为空。
    in_userid: Mapped[Optional[str]] = mapped_column("in_userid", String(64))
    # [2026-07-04 10:18:20] 作用：保存意图入库时间；理由依据：验收需定位本次新增记录。
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column("in_time", DateTime)
    # [2026-07-04 10:18:20] 作用：映射数据库保留列 yima；理由依据：实际表含该列且原业务没有赋值语义。
    yima: Mapped[Optional[str]] = mapped_column("yima", String(64))

# [2026-07-04 10:18:20] 作用：声明原始数据 ORM；理由依据：音频转录全文及来源信息必须先写入 AI_YuanShishuju。
class ErpYuanShiShuJu(Base):
    # [2026-07-04 10:18:20] 作用：指定原始数据表精确名称；理由依据：PostgreSQL 使用带引号的混合大小写表名。
    __tablename__ = "AI_YuanShishuju"
    # [2026-07-04 10:18:20] 作用：开始配置原始数据复合主键；理由依据：实际表由 shuju_id 与 GuanLianKeHu 联合唯一。
    __table_args__ = (
        # [2026-07-04 10:18:20] 作用：声明原始数据复合主键；理由依据：阻止同一来源 ID 与客户组合重复入库。
        PrimaryKeyConstraint("shuju_id", "GuanLianKeHu", name="pk_AI_YuanShishuju"),
    # [2026-07-04 10:18:20] 作用：结束原始数据约束配置；理由依据：形成合法的表级参数元组。
    )
    # [2026-07-04 10:18:20] 作用：映射原始数据 UUID7；理由依据：该 ID 是问答和意图的统一外部关联键。
    shuju_id: Mapped[str] = mapped_column("shuju_id", String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-04 10:18:20] 作用：保存资产类型 ID；理由依据：来源为 multipart asset_type_id。
    ZcLeiXin: Mapped[Optional[str]] = mapped_column("ZcLeiXin", String(64))
    # [2026-07-04 10:18:20] 作用：保存完整音频转录全文；理由依据：目标列为 text，无需制造会冲突的分块主键。
    ShuJu: Mapped[Optional[str]] = mapped_column("ShuJu", Text)
    # [2026-07-04 10:18:20] 作用：保存服务端处理文件路径；理由依据：沿用原项目来源追踪语义。
    WenJianDiZhi: Mapped[Optional[str]] = mapped_column("WenJianDiZhi", Text)
    # [2026-07-04 10:18:20] 作用：保存上传原文件名；理由依据：验收需精确识别 `新录音 4.m4a`。
    WenJianName: Mapped[Optional[str]] = mapped_column("WenJianName", Text)
    # [2026-07-04 10:18:20] 作用：保存来源类型码；理由依据：audio 固定映射为整数 3。
    LaiYuan: Mapped[Optional[int]] = mapped_column("LaiYuan", Integer)
    # [2026-07-04 10:18:20] 作用：保存关联客户复合主键；理由依据：实际列为 varchar(64)，不能沿用旧整数声明。
    GuanLianKeHu: Mapped[str] = mapped_column("GuanLianKeHu", String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-04 10:18:20] 作用：保存企业 ID；理由依据：当前无企业上下文时允许为空且实际列为 varchar(64)。
    gs_id: Mapped[Optional[str]] = mapped_column("gs_id", String(64))
    # [2026-07-04 10:18:20] 作用：保存逻辑删除标志；理由依据：新增有效记录必须为 false。
    del_flag: Mapped[bool] = mapped_column("del_flag", Boolean, nullable=False, server_default=text("FALSE"))
    # [2026-07-04 10:18:20] 作用：保存删除时间；理由依据：新增有效记录尚未删除时为空。
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column("del_time", DateTime)
    # [2026-07-04 10:18:20] 作用：保存录入用户 ID；理由依据：当前独立 WebUI 无登录用户时允许为空。
    in_userid: Mapped[Optional[str]] = mapped_column("in_userid", String(64))
    # [2026-07-04 10:18:20] 作用：保存原始数据入库时间；理由依据：验收需按时间窗口核对新增行。
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column("in_time", DateTime)
    # [2026-07-04 10:18:20] 作用：保存修改用户 ID；理由依据：新记录尚未修改时为空。
    up_userid: Mapped[Optional[str]] = mapped_column("up_userid", String(64))
    # [2026-07-04 10:18:20] 作用：保存修改时间；理由依据：新记录尚未修改时为空。
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column("up_time", DateTime)
    # [2026-07-04 10:18:20] 作用：映射数据库保留列 yima；理由依据：实际表含该列且原业务没有赋值语义。
    yima: Mapped[Optional[str]] = mapped_column("yima", String(64))
