# [2026-07-03 18:11:51] 作用：导入依赖 `from typing import Optional`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from typing import Optional
# [2026-07-03 18:11:51] 作用：导入依赖 `import datetime`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
import datetime
# [2026-07-03 18:11:51] 作用：导入依赖 `import decimal`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
import decimal
# [2026-07-03 18:11:51] 作用：导入依赖 `from sqlalchemy import (`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from sqlalchemy import (
    # [2026-07-03 18:11:51] 作用：在 模块级初始化 中执行具体代码片段 `BigInteger,`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    BigInteger,
    # [2026-07-03 18:11:51] 作用：在 模块级初始化 中执行具体代码片段 `Boolean,`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    Boolean,
    # [2026-07-03 18:11:51] 作用：在 模块级初始化 中执行具体代码片段 `DateTime,`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    DateTime,
    # [2026-07-03 18:11:51] 作用：在 模块级初始化 中执行具体代码片段 `DECIMAL,`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    DECIMAL,
    # [2026-07-03 18:11:51] 作用：在 模块级初始化 中执行具体代码片段 `Integer,`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    Integer,
    # [2026-07-03 18:11:51] 作用：在 模块级初始化 中执行具体代码片段 `PrimaryKeyConstraint,`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    PrimaryKeyConstraint,
    # [2026-07-03 18:11:51] 作用：在 模块级初始化 中执行具体代码片段 `SmallInteger,`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    SmallInteger,
    # [2026-07-03 18:11:51] 作用：在 模块级初始化 中执行具体代码片段 `String,`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    String,
    # [2026-07-03 18:11:51] 作用：在 模块级初始化 中执行具体代码片段 `Text,`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    Text,
    # [2026-07-03 18:11:51] 作用：在 模块级初始化 中执行具体代码片段 `text,`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
    text,
# [2026-07-03 18:11:51] 作用：在 模块级初始化 中执行具体代码片段 `)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
)
# [2026-07-03 18:11:51] 作用：导入依赖 `from sqlalchemy.orm import Mapped, mapped_column`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from sqlalchemy.orm import Mapped, mapped_column
# [2026-07-03 18:11:51] 作用：导入依赖 `from extraction_chain.model_base import Base`，供 模块级初始化 使用；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行属于模块级初始化
from extraction_chain.model_base import Base
# [2026-07-03 18:11:51] 作用：声明类 ErpWendaJilu，封装该节点的数据结构与行为；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
class ErpWendaJilu(Base):
    # [2026-07-03 18:11:51] 作用：为 __tablename__ 指定 ORM 对应数据库表；本行设置 `__tablename__ = "AI_Wendajilu"`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    __tablename__ = "AI_Wendajilu"
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `__table_args__ = (`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    __table_args__ = (
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `PrimaryKeyConstraint('wdjl_ id', 'Yssj_id', name="pk_AI_Wendajilu"),`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
        PrimaryKeyConstraint('wdjl_ id', 'Yssj_id', name="pk_AI_Wendajilu"),
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `{"comment": "Generated ORM for AI_Wendajilu"},`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
        {"comment": "Generated ORM for AI_Wendajilu"},
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    )
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 wdjl_id 的数据库列类型和约束；本行设置 `wdjl_id: Mapped[int] = mapped_column('wdjl_ id', String(64), primary_key=True, autoincrement=Fa…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    wdjl_id: Mapped[int] = mapped_column('wdjl_ id', String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 Yssj_id 的数据库列类型和约束；本行设置 `Yssj_id: Mapped[int] = mapped_column('Yssj_id', String(64), primary_key=True, autoincrement=Fal…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    Yssj_id: Mapped[int] = mapped_column('Yssj_id', String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 AI_WenTi 的数据库列类型和约束；本行设置 `AI_WenTi: Mapped[Optional[str]] = mapped_column('AI_WenTi', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    AI_WenTi: Mapped[Optional[str]] = mapped_column('AI_WenTi', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 AI_DaAn 的数据库列类型和约束；本行设置 `AI_DaAn: Mapped[Optional[str]] = mapped_column('AI_DaAn', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    AI_DaAn: Mapped[Optional[str]] = mapped_column('AI_DaAn', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 AI_Biaozhu 的数据库列类型和约束；本行设置 `AI_Biaozhu: Mapped[Optional[str]] = mapped_column('AI_Biaozhu', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    AI_Biaozhu: Mapped[Optional[str]] = mapped_column('AI_Biaozhu', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 WenTiYuanWen 的数据库列类型和约束；本行设置 `WenTiYuanWen: Mapped[Optional[str]] = mapped_column('WenTiYuanWen', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    WenTiYuanWen: Mapped[Optional[str]] = mapped_column('WenTiYuanWen', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 DaAnYuanWen 的数据库列类型和约束；本行设置 `DaAnYuanWen: Mapped[Optional[str]] = mapped_column('DaAnYuanWen', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    DaAnYuanWen: Mapped[Optional[str]] = mapped_column('DaAnYuanWen', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 WenTi_true 的数据库列类型和约束；本行设置 `WenTi_true: Mapped[Optional[str]] = mapped_column('WenTi_true', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    WenTi_true: Mapped[Optional[str]] = mapped_column('WenTi_true', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 DaAn_true 的数据库列类型和约束；本行设置 `DaAn_true: Mapped[Optional[str]] = mapped_column('DaAn_true', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    DaAn_true: Mapped[Optional[str]] = mapped_column('DaAn_true', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 Biaozhu_true 的数据库列类型和约束；本行设置 `Biaozhu_true: Mapped[Optional[str]] = mapped_column('Biaozhu_true', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    Biaozhu_true: Mapped[Optional[str]] = mapped_column('Biaozhu_true', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ZhuangTai 的数据库列类型和约束；本行设置 `ZhuangTai: Mapped[Optional[int]] = mapped_column('ZhuangTai', Integer)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    ZhuangTai: Mapped[Optional[int]] = mapped_column('ZhuangTai', Integer)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ZhuangTai_id 的数据库列类型和约束；本行设置 `ZhuangTai_id: Mapped[Optional[int]] = mapped_column('ZhuangTai_id', Integer)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    ZhuangTai_id: Mapped[Optional[int]] = mapped_column('ZhuangTai_id', Integer)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ZhuangTai_time 的数据库列类型和约束；本行设置 `ZhuangTai_time: Mapped[Optional[datetime.datetime]] = mapped_column('ZhuangTai_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    ZhuangTai_time: Mapped[Optional[datetime.datetime]] = mapped_column('ZhuangTai_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 YinPinShiJian 的数据库列类型和约束；本行设置 `YinPinShiJian: Mapped[Optional[str]] = mapped_column('YinPinShiJian', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    YinPinShiJian: Mapped[Optional[str]] = mapped_column('YinPinShiJian', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gsId 的数据库列类型和约束；本行设置 `gsId: Mapped[Optional[int]] = mapped_column('gsId', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    gsId: Mapped[Optional[int]] = mapped_column('gsId', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_userid 的数据库列类型和约束；本行设置 `in_userid: Mapped[Optional[int]] = mapped_column('in_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    in_userid: Mapped[Optional[int]] = mapped_column('in_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_time 的数据库列类型和约束；本行设置 `in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpWendaJilu
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
# [2026-07-03 18:11:51] 作用：声明类 ErpYitu，封装该节点的数据结构与行为；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
class ErpYitu(Base):
    # [2026-07-03 18:11:51] 作用：为 __tablename__ 指定 ORM 对应数据库表；本行设置 `__tablename__ = "AI_Yitu"`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    __tablename__ = "AI_Yitu"
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `__table_args__ = (`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    __table_args__ = (
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `PrimaryKeyConstraint('yt_ id', 'Yssj_id', name="pk_AI_Yitu"),`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
        PrimaryKeyConstraint('yt_ id', 'Yssj_id', name="pk_AI_Yitu"),
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `{"comment": "Generated ORM for AI_Yitu"},`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
        {"comment": "Generated ORM for AI_Yitu"},
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    )
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 yt_id 的数据库列类型和约束；本行设置 `yt_id: Mapped[int] = mapped_column('yt_ id', String(64), primary_key=True, autoincrement=False,…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    yt_id: Mapped[int] = mapped_column('yt_ id', String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 Yssj_id 的数据库列类型和约束；本行设置 `Yssj_id: Mapped[int] = mapped_column('Yssj_id', String(64), primary_key=True, autoincrement=Fal…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    Yssj_id: Mapped[int] = mapped_column('Yssj_id', String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 AI_YiTu 的数据库列类型和约束；本行设置 `AI_YiTu: Mapped[Optional[str]] = mapped_column('AI_YiTu', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    AI_YiTu: Mapped[Optional[str]] = mapped_column('AI_YiTu', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 YiTu 的数据库列类型和约束；本行设置 `YiTu: Mapped[Optional[str]] = mapped_column('YiTu', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    YiTu: Mapped[Optional[str]] = mapped_column('YiTu', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 BiaoZhu 的数据库列类型和约束；本行设置 `BiaoZhu: Mapped[Optional[str]] = mapped_column('BiaoZhu', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    BiaoZhu: Mapped[Optional[str]] = mapped_column('BiaoZhu', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ZhuangTai 的数据库列类型和约束；本行设置 `ZhuangTai: Mapped[Optional[int]] = mapped_column('ZhuangTai', Integer)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    ZhuangTai: Mapped[Optional[int]] = mapped_column('ZhuangTai', Integer)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ZhuangTai_id 的数据库列类型和约束；本行设置 `ZhuangTai_id: Mapped[Optional[int]] = mapped_column('ZhuangTai_id', Integer)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    ZhuangTai_id: Mapped[Optional[int]] = mapped_column('ZhuangTai_id', Integer)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ZhuangTai_time 的数据库列类型和约束；本行设置 `ZhuangTai_time: Mapped[Optional[datetime.datetime]] = mapped_column('ZhuangTai_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    ZhuangTai_time: Mapped[Optional[datetime.datetime]] = mapped_column('ZhuangTai_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ShiJian 的数据库列类型和约束；本行设置 `ShiJian: Mapped[Optional[str]] = mapped_column('ShiJian', String(255))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    ShiJian: Mapped[Optional[str]] = mapped_column('ShiJian', String(255))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gsId 的数据库列类型和约束；本行设置 `gsId: Mapped[Optional[int]] = mapped_column('gsId', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    gsId: Mapped[Optional[int]] = mapped_column('gsId', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_time 的数据库列类型和约束；本行设置 `del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_userid 的数据库列类型和约束；本行设置 `in_userid: Mapped[Optional[int]] = mapped_column('in_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    in_userid: Mapped[Optional[int]] = mapped_column('in_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_time 的数据库列类型和约束；本行设置 `in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYitu
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
# [2026-07-03 18:11:51] 作用：声明类 ErpYuanShiShuJu，封装该节点的数据结构与行为；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
class ErpYuanShiShuJu(Base):
    # [2026-07-03 18:11:51] 作用：为 __tablename__ 指定 ORM 对应数据库表；本行设置 `__tablename__ = "AI_YuanShishuju"`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    __tablename__ = "AI_YuanShishuju"
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `__table_args__ = (`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    __table_args__ = (
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `PrimaryKeyConstraint('shuju_id', 'GuanLianKeHu', name="pk_AI_YuanShishuju"),`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
        PrimaryKeyConstraint('shuju_id', 'GuanLianKeHu', name="pk_AI_YuanShishuju"),
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `{"comment": "Generated ORM for AI_YuanShishuju"},`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
        {"comment": "Generated ORM for AI_YuanShishuju"},
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    )
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 shuju_id 的数据库列类型和约束；本行设置 `shuju_id: Mapped[str] = mapped_column('shuju_id', String(64), primary_key=True, autoincrement=F…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    shuju_id: Mapped[str] = mapped_column('shuju_id', String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ZcLeiXin 的数据库列类型和约束；本行设置 `ZcLeiXin: Mapped[Optional[str]] = mapped_column('ZcLeiXin', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    ZcLeiXin: Mapped[Optional[str]] = mapped_column('ZcLeiXin', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ShuJu 的数据库列类型和约束；本行设置 `ShuJu: Mapped[Optional[str]] = mapped_column('ShuJu', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    ShuJu: Mapped[Optional[str]] = mapped_column('ShuJu', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 WenJianDiZhi 的数据库列类型和约束；本行设置 `WenJianDiZhi: Mapped[Optional[str]] = mapped_column('WenJianDiZhi', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    WenJianDiZhi: Mapped[Optional[str]] = mapped_column('WenJianDiZhi', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 WenJianName 的数据库列类型和约束；本行设置 `WenJianName: Mapped[Optional[str]] = mapped_column('WenJianName', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    WenJianName: Mapped[Optional[str]] = mapped_column('WenJianName', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 LaiYuan 的数据库列类型和约束；本行设置 `LaiYuan: Mapped[Optional[int]] = mapped_column('LaiYuan', Integer)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    LaiYuan: Mapped[Optional[int]] = mapped_column('LaiYuan', Integer)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 GuanLianKeHu 的数据库列类型和约束；本行设置 `GuanLianKeHu: Mapped[int] = mapped_column('GuanLianKeHu', Integer, primary_key=True, autoincrem…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    GuanLianKeHu: Mapped[int] = mapped_column('GuanLianKeHu', Integer, primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gs_id 的数据库列类型和约束；本行设置 `gs_id: Mapped[Optional[str]] = mapped_column('gs_id', Integer)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    gs_id: Mapped[Optional[str]] = mapped_column('gs_id', Integer)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_flag 的数据库列类型和约束；本行设置 `del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False, server_default=text…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False, server_default=text('FALSE'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_time 的数据库列类型和约束；本行设置 `del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_userid 的数据库列类型和约束；本行设置 `in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_time 的数据库列类型和约束；本行设置 `in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 up_userid 的数据库列类型和约束；本行设置 `up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 up_time 的数据库列类型和约束；本行设置 `up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpYuanShiShuJu
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)
# [2026-07-03 18:11:51] 作用：声明类 ErpGongSi，封装该节点的数据结构与行为；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
class ErpGongSi(Base):
    # [2026-07-03 18:11:51] 作用：为 __tablename__ 指定 ORM 对应数据库表；本行设置 `__tablename__ = "AI_GongSi"`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    __tablename__ = "AI_GongSi"
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `__table_args__ = (`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    __table_args__ = (
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `PrimaryKeyConstraint('gsId', name="pk_AI_GongSi"),`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
        PrimaryKeyConstraint('gsId', name="pk_AI_GongSi"),
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `{"comment": "Generated ORM for AI_GongSi"},`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
        {"comment": "Generated ORM for AI_GongSi"},
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    )
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gsId 的数据库列类型和约束；本行设置 `gsId: Mapped[str] = mapped_column('gsId',String(64), primary_key=True, autoincrement=False, nul…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    gsId: Mapped[str] = mapped_column('gsId',String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gongSiDaiMa 的数据库列类型和约束；本行设置 `gongSiDaiMa: Mapped[Optional[str]] = mapped_column('gongSiDaiMa', String(255))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    gongSiDaiMa: Mapped[Optional[str]] = mapped_column('gongSiDaiMa', String(255))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gongSiQuanCheng 的数据库列类型和约束；本行设置 `gongSiQuanCheng: Mapped[Optional[str]] = mapped_column('gongSiQuanCheng', String(255))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    gongSiQuanCheng: Mapped[Optional[str]] = mapped_column('gongSiQuanCheng', String(255))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gongSiJianCheng 的数据库列类型和约束；本行设置 `gongSiJianCheng: Mapped[Optional[str]] = mapped_column('gongSiJianCheng', String(50))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    gongSiJianCheng: Mapped[Optional[str]] = mapped_column('gongSiJianCheng', String(50))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gongSiDiZhi 的数据库列类型和约束；本行设置 `gongSiDiZhi: Mapped[Optional[str]] = mapped_column('gongSiDiZhi', String(255))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    gongSiDiZhi: Mapped[Optional[str]] = mapped_column('gongSiDiZhi', String(255))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_flag 的数据库列类型和约束；本行设置 `del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False, server_default=text…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False, server_default=text('FALSE'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_time 的数据库列类型和约束；本行设置 `del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_userid 的数据库列类型和约束；本行设置 `in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_time 的数据库列类型和约束；本行设置 `in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 up_userid 的数据库列类型和约束；本行设置 `up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 up_time 的数据库列类型和约束；本行设置 `up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 ErpGongSi
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)
# [2026-07-03 18:11:51] 作用：声明类 AILiaoTianZhu，封装该节点的数据结构与行为；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
class AILiaoTianZhu(Base):
    # [2026-07-03 18:11:51] 作用：为 __tablename__ 指定 ORM 对应数据库表；本行设置 `__tablename__ = "AI_liaotianzhu"`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
    __tablename__ = "AI_liaotianzhu"
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `__table_args__ = (`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
    __table_args__ = (
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `PrimaryKeyConstraint('Ltz_id', name="pk_AI_liaotianzhu"),`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
        PrimaryKeyConstraint('Ltz_id', name="pk_AI_liaotianzhu"),
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `{"comment": "Generated ORM for AI_liaotianzhu"},`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
        {"comment": "Generated ORM for AI_liaotianzhu"},
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
    )
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 Ltz_id 的数据库列类型和约束；本行设置 `Ltz_id: Mapped[str] = mapped_column('Ltz_id', String(64), primary_key=True, autoincrement=False…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
    Ltz_id: Mapped[str] = mapped_column('Ltz_id', String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 session_id 的数据库列类型和约束；本行设置 `session_id: Mapped[str] = mapped_column('session_id', String(64), nullable=False)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
    session_id: Mapped[str] = mapped_column('session_id', String(64), nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 create_at 的数据库列类型和约束；本行设置 `create_at: Mapped[Optional[datetime.datetime]] = mapped_column('create_at', DateTime, server_de…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column('create_at', DateTime, server_default=text('CURRENT_TIMESTAMP'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_time 的数据库列类型和约束；本行设置 `del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_flag 的数据库列类型和约束；本行设置 `del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
    del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gsyh_id 的数据库列类型和约束；本行设置 `gsyh_id: Mapped[str] = mapped_column('gsyh_id', String(64), nullable=False)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
    gsyh_id: Mapped[str] = mapped_column('gsyh_id', String(64), nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gs_id 的数据库列类型和约束；本行设置 `gs_id: Mapped[str] = mapped_column('gs_id', String(64), nullable=False)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
    gs_id: Mapped[str] = mapped_column('gs_id', String(64), nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 title 的数据库列类型和约束；本行设置 `title: Mapped[Optional[str]] = mapped_column('title', String(255))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianZhu
    title: Mapped[Optional[str]] = mapped_column('title', String(255))
# [2026-07-03 18:11:51] 作用：声明类 AILiaoTianJiLu，封装该节点的数据结构与行为；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
class AILiaoTianJiLu(Base):
    # [2026-07-03 18:11:51] 作用：为 __tablename__ 指定 ORM 对应数据库表；本行设置 `__tablename__ = "AI_liaotianjilu"`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    __tablename__ = "AI_liaotianjilu"
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `__table_args__ = (`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    __table_args__ = (
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `PrimaryKeyConstraint("ltjlid", name="pk_AI_liaotianjilu"),`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
        PrimaryKeyConstraint("ltjlid", name="pk_AI_liaotianjilu"),
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `{"comment": "Generated ORM for AI_liaotianjilu"},`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
        {"comment": "Generated ORM for AI_liaotianjilu"},
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    )
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ltjlid 的数据库列类型和约束；本行设置 `ltjlid: Mapped[str] = mapped_column("ltjlid", String(64), primary_key=True, autoincrement=False…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    ltjlid: Mapped[str] = mapped_column("ltjlid", String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ltz_id 的数据库列类型和约束；本行设置 `ltz_id: Mapped[str] = mapped_column("ltz_id", String(64), nullable=False, index=True)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    ltz_id: Mapped[str] = mapped_column("ltz_id", String(64), nullable=False, index=True)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 message_role 的数据库列类型和约束；本行设置 `message_role: Mapped[str] = mapped_column("message_role", String(10), nullable=False)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    message_role: Mapped[str] = mapped_column("message_role", String(10), nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 message_content 的数据库列类型和约束；本行设置 `message_content: Mapped[str] = mapped_column("message_content", Text, nullable=False)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    message_content: Mapped[str] = mapped_column("message_content", Text, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 Moshi 的数据库列类型和约束；本行设置 `Moshi: Mapped[Optional[int]] = mapped_column("Moshi", Integer)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    Moshi: Mapped[Optional[int]] = mapped_column("Moshi", Integer)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 Wenjian_id 的数据库列类型和约束；本行设置 `Wenjian_id: Mapped[Optional[str]] = mapped_column("Wenjian_id", String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    Wenjian_id: Mapped[Optional[str]] = mapped_column("Wenjian_id", String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 PingJia 的数据库列类型和约束；本行设置 `PingJia: Mapped[Optional[str]] = mapped_column("PingJia", String(255))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    PingJia: Mapped[Optional[str]] = mapped_column("PingJia", String(255))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 create_at 的数据库列类型和约束；本行设置 `create_at: Mapped[Optional[datetime.datetime]] = mapped_column("create_at", DateTime, server_de…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP"))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gx_create_at 的数据库列类型和约束；本行设置 `gx_create_at: Mapped[Optional[datetime.datetime]] = mapped_column("gx_create_at", DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    gx_create_at: Mapped[Optional[datetime.datetime]] = mapped_column("gx_create_at", DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_time 的数据库列类型和约束；本行设置 `del_time: Mapped[Optional[datetime.datetime]] = mapped_column("del_time", DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column("del_time", DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_flag 的数据库列类型和约束；本行设置 `del_flag: Mapped[bool] = mapped_column("del_flag", Boolean, nullable=False)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AILiaoTianJiLu
    del_flag: Mapped[bool] = mapped_column("del_flag", Boolean, nullable=False)
# [2026-07-03 18:11:51] 作用：声明类 AIGongSiYongHu，封装该节点的数据结构与行为；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
class AIGongSiYongHu(Base):
    # [2026-07-03 18:11:51] 作用：为 __tablename__ 指定 ORM 对应数据库表；本行设置 `__tablename__ = "AI_GongSiYongHu"`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    __tablename__ = "AI_GongSiYongHu"
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `__table_args__ = (`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    __table_args__ = (
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `PrimaryKeyConstraint('gsyhId', name="pk_AI_GongSiYongHu"),`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
        PrimaryKeyConstraint('gsyhId', name="pk_AI_GongSiYongHu"),
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `{"comment": "Generated ORM for AI_GongSiYongHu"},`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
        {"comment": "Generated ORM for AI_GongSiYongHu"},
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    )
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gsyhId 的数据库列类型和约束；本行设置 `gsyhId: Mapped[str] = mapped_column('gsyhId', String(64), primary_key=True, autoincrement=False…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    gsyhId: Mapped[str] = mapped_column('gsyhId', String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 yongHuXingMing 的数据库列类型和约束；本行设置 `yongHuXingMing: Mapped[Optional[str]] = mapped_column('yongHuXingMing', String(255))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    yongHuXingMing: Mapped[Optional[str]] = mapped_column('yongHuXingMing', String(255))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 xingBie 的数据库列类型和约束；本行设置 `xingBie: Mapped[Optional[int]] = mapped_column('xingBie', SmallInteger, server_default=text('0'…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    xingBie: Mapped[Optional[int]] = mapped_column('xingBie', SmallInteger, server_default=text('0'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 dianHua 的数据库列类型和约束；本行设置 `dianHua: Mapped[Optional[str]] = mapped_column('dianHua', String(11))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    dianHua: Mapped[Optional[str]] = mapped_column('dianHua', String(11))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gsId 的数据库列类型和约束；本行设置 `gsId: Mapped[Optional[str]] = mapped_column('gsId', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    gsId: Mapped[Optional[str]] = mapped_column('gsId', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_flag 的数据库列类型和约束；本行设置 `del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False, server_default=text…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False, server_default=text('FALSE'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_time 的数据库列类型和约束；本行设置 `del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_userid 的数据库列类型和约束；本行设置 `in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_time 的数据库列类型和约束；本行设置 `in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 up_userid 的数据库列类型和约束；本行设置 `up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 up_time 的数据库列类型和约束；本行设置 `up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIGongSiYongHu
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)
# [2026-07-03 18:11:51] 作用：声明类 AIYongHuShiYongTongJi，封装该节点的数据结构与行为；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
class AIYongHuShiYongTongJi(Base):
    # [2026-07-03 18:11:51] 作用：为 __tablename__ 指定 ORM 对应数据库表；本行设置 `__tablename__ = "AI_YongHuShiYongTongJi"`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    __tablename__ = "AI_YongHuShiYongTongJi"
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `__table_args__ = (`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    __table_args__ = (
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `PrimaryKeyConstraint('syjlId', name="pk_AI_YongHuShiYongTongJi"),`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
        PrimaryKeyConstraint('syjlId', name="pk_AI_YongHuShiYongTongJi"),
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `{"comment": "Generated ORM for AI_YongHuShiYongTongJi"},`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
        {"comment": "Generated ORM for AI_YongHuShiYongTongJi"},
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    )
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 syjlId 的数据库列类型和约束；本行设置 `syjlId: Mapped[str] = mapped_column('syjlId', String(64), primary_key=True, autoincrement=False…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    syjlId: Mapped[str] = mapped_column('syjlId', String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 yongHuId 的数据库列类型和约束；本行设置 `yongHuId: Mapped[Optional[str]] = mapped_column('yongHuId', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    yongHuId: Mapped[Optional[str]] = mapped_column('yongHuId', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gsId 的数据库列类型和约束；本行设置 `gsId: Mapped[str] = mapped_column('gsId', BigInteger, nullable=False)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    gsId: Mapped[str] = mapped_column('gsId', BigInteger, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 buMenId 的数据库列类型和约束；本行设置 `buMenId: Mapped[Optional[int]] = mapped_column('buMenId', BigInteger)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    buMenId: Mapped[Optional[int]] = mapped_column('buMenId', BigInteger)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 session_id 的数据库列类型和约束；本行设置 `session_id: Mapped[Optional[str]] = mapped_column('session_id', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    session_id: Mapped[Optional[str]] = mapped_column('session_id', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ai_gongNeng 的数据库列类型和约束；本行设置 `ai_gongNeng: Mapped[Optional[str]] = mapped_column('ai_gongNeng', String(100))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    ai_gongNeng: Mapped[Optional[str]] = mapped_column('ai_gongNeng', String(100))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 yeWuChangJing 的数据库列类型和约束；本行设置 `yeWuChangJing: Mapped[Optional[str]] = mapped_column('yeWuChangJing', String(100))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    yeWuChangJing: Mapped[Optional[str]] = mapped_column('yeWuChangJing', String(100))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 wenTiLeiXing 的数据库列类型和约束；本行设置 `wenTiLeiXing: Mapped[Optional[str]] = mapped_column('wenTiLeiXing', String(100))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    wenTiLeiXing: Mapped[Optional[str]] = mapped_column('wenTiLeiXing', String(100))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 tiWenNeiRong 的数据库列类型和约束；本行设置 `tiWenNeiRong: Mapped[Optional[str]] = mapped_column('tiWenNeiRong', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    tiWenNeiRong: Mapped[Optional[str]] = mapped_column('tiWenNeiRong', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 aiHuiDaNeiRong 的数据库列类型和约束；本行设置 `aiHuiDaNeiRong: Mapped[Optional[str]] = mapped_column('aiHuiDaNeiRong', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    aiHuiDaNeiRong: Mapped[Optional[str]] = mapped_column('aiHuiDaNeiRong', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 shiFouCaiNa 的数据库列类型和约束；本行设置 `shiFouCaiNa: Mapped[Optional[bool]] = mapped_column('shiFouCaiNa', Boolean, server_default=text…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    shiFouCaiNa: Mapped[Optional[bool]] = mapped_column('shiFouCaiNa', Boolean, server_default=text('FALSE'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 caiNaFangShi 的数据库列类型和约束；本行设置 `caiNaFangShi: Mapped[Optional[str]] = mapped_column('caiNaFangShi', String(50))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    caiNaFangShi: Mapped[Optional[str]] = mapped_column('caiNaFangShi', String(50))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 qingQiuToken 的数据库列类型和约束；本行设置 `qingQiuToken: Mapped[Optional[int]] = mapped_column('qingQiuToken', Integer)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    qingQiuToken: Mapped[Optional[int]] = mapped_column('qingQiuToken', Integer)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 huiDaToken 的数据库列类型和约束；本行设置 `huiDaToken: Mapped[Optional[int]] = mapped_column('huiDaToken', Integer)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    huiDaToken: Mapped[Optional[int]] = mapped_column('huiDaToken', Integer)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 feiYong 的数据库列类型和约束；本行设置 `feiYong: Mapped[Optional[decimal.Decimal]] = mapped_column('feiYong', DECIMAL(18, 6))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    feiYong: Mapped[Optional[decimal.Decimal]] = mapped_column('feiYong', DECIMAL(18, 6))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 shiYongShiJian 的数据库列类型和约束；本行设置 `shiYongShiJian: Mapped[datetime.datetime] = mapped_column('shiYongShiJian', DateTime, nullable=…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    shiYongShiJian: Mapped[datetime.datetime] = mapped_column('shiYongShiJian', DateTime, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_flag 的数据库列类型和约束；本行设置 `del_flag: Mapped[Optional[bool]] = mapped_column('del_flag', Boolean, server_default=text('FALS…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    del_flag: Mapped[Optional[bool]] = mapped_column('del_flag', Boolean, server_default=text('FALSE'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_time 的数据库列类型和约束；本行设置 `del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_userid 的数据库列类型和约束；本行设置 `in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_time 的数据库列类型和约束；本行设置 `in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 up_userid 的数据库列类型和约束；本行设置 `up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 up_time 的数据库列类型和约束；本行设置 `up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIYongHuShiYongTongJi
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)
# [2026-07-03 18:11:51] 作用：声明类 AITiShiCiGuanLiBiao，封装该节点的数据结构与行为；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
class AITiShiCiGuanLiBiao(Base):
    # [2026-07-03 18:11:51] 作用：为 __tablename__ 指定 ORM 对应数据库表；本行设置 `__tablename__ = "AI_erp_TiShiCiGuanLiBiao"`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    __tablename__ = "AI_erp_TiShiCiGuanLiBiao"
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `__table_args__ = (`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    __table_args__ = (
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `PrimaryKeyConstraint('tscId', name="pk_AI_erp_TiShiCiGuanLiBiao"),`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
        PrimaryKeyConstraint('tscId', name="pk_AI_erp_TiShiCiGuanLiBiao"),
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `{"comment": "Generated ORM for AI_erp_TiShiCiGuanLiBiao"},`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
        {"comment": "Generated ORM for AI_erp_TiShiCiGuanLiBiao"},
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    )
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 tscId 的数据库列类型和约束；本行设置 `tscId: Mapped[str] = mapped_column('tscId', String(64), primary_key=True, autoincrement=False, …`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    tscId: Mapped[str] = mapped_column('tscId', String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 systemPrompt 的数据库列类型和约束；本行设置 `systemPrompt: Mapped[Optional[str]] = mapped_column('systemPrompt', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    systemPrompt: Mapped[Optional[str]] = mapped_column('systemPrompt', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 UsermPrompt 的数据库列类型和约束；本行设置 `UsermPrompt: Mapped[str] = mapped_column('UsermPrompt', Text, nullable=False)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    UsermPrompt: Mapped[str] = mapped_column('UsermPrompt', Text, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ShuChuGeShi 的数据库列类型和约束；本行设置 `ShuChuGeShi: Mapped[Optional[str]] = mapped_column('ShuChuGeShi', Text)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    ShuChuGeShi: Mapped[Optional[str]] = mapped_column('ShuChuGeShi', Text)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 tiShiCiBianMa 的数据库列类型和约束；本行设置 `tiShiCiBianMa: Mapped[str] = mapped_column('tiShiCiBianMa', String(100), nullable=False)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    tiShiCiBianMa: Mapped[str] = mapped_column('tiShiCiBianMa', String(100), nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 TiShiCiZhuangTai 的数据库列类型和约束；本行设置 `TiShiCiZhuangTai: Mapped[Optional[int]] = mapped_column('TiShiCiZhuangTai', Integer)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    TiShiCiZhuangTai: Mapped[Optional[int]] = mapped_column('TiShiCiZhuangTai', Integer)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 Tishicileixing 的数据库列类型和约束；本行设置 `Tishicileixing: Mapped[Optional[int]] = mapped_column('Tishicileixing', Integer)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    Tishicileixing: Mapped[Optional[int]] = mapped_column('Tishicileixing', Integer)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gsId 的数据库列类型和约束；本行设置 `gsId: Mapped[Optional[str]] = mapped_column('gsId', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    gsId: Mapped[Optional[str]] = mapped_column('gsId', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_flag 的数据库列类型和约束；本行设置 `del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False, server_default=text…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False, server_default=text('FALSE'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_time 的数据库列类型和约束；本行设置 `del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_userid 的数据库列类型和约束；本行设置 `in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_time 的数据库列类型和约束；本行设置 `in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 up_userid 的数据库列类型和约束；本行设置 `up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 up_time 的数据库列类型和约束；本行设置 `up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AITiShiCiGuanLiBiao
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)
# [2026-07-03 18:11:51] 作用：声明类 AIZiChanLeiXing，封装该节点的数据结构与行为；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
class AIZiChanLeiXing(Base):
    # [2026-07-03 18:11:51] 作用：为 __tablename__ 指定 ORM 对应数据库表；本行设置 `__tablename__ = "AI_ZiChanLeiXing"`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    __tablename__ = "AI_ZiChanLeiXing"
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `__table_args__ = (`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    __table_args__ = (
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `PrimaryKeyConstraint('zclxId', name="pk_AI_ZiChanLeiXing"),`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
        PrimaryKeyConstraint('zclxId', name="pk_AI_ZiChanLeiXing"),
        # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `{"comment": "Generated ORM for AI_ZiChanLeiXing"},`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
        {"comment": "Generated ORM for AI_ZiChanLeiXing"},
    # [2026-07-03 18:11:51] 作用：为 __table_args__ 配置 ORM 表级主键、索引或约束；本行设置 `)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    )
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 zclxId 的数据库列类型和约束；本行设置 `zclxId: Mapped[str] = mapped_column('zclxId', String(64), primary_key=True, autoincrement=False…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    zclxId: Mapped[str] = mapped_column('zclxId', String(64), primary_key=True, autoincrement=False, nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 gsId 的数据库列类型和约束；本行设置 `gsId: Mapped[str] = mapped_column('gsId', String(64), nullable=False)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    gsId: Mapped[str] = mapped_column('gsId', String(64), nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ziChanLeiXing 的数据库列类型和约束；本行设置 `ziChanLeiXing: Mapped[str] = mapped_column('ziChanLeiXing', String(100), nullable=False)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    ziChanLeiXing: Mapped[str] = mapped_column('ziChanLeiXing', String(100), nullable=False)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 ziChanShuoMing 的数据库列类型和约束；本行设置 `ziChanShuoMing: Mapped[Optional[str]] = mapped_column('ziChanShuoMing', String(500))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    ziChanShuoMing: Mapped[Optional[str]] = mapped_column('ziChanShuoMing', String(500))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 zhiShiShuLiang 的数据库列类型和约束；本行设置 `zhiShiShuLiang: Mapped[Optional[int]] = mapped_column('zhiShiShuLiang', Integer, server_default…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    zhiShiShuLiang: Mapped[Optional[int]] = mapped_column('zhiShiShuLiang', Integer, server_default=text('0'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 guanLiQuanXian 的数据库列类型和约束；本行设置 `guanLiQuanXian: Mapped[Optional[str]] = mapped_column('guanLiQuanXian', String(100))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    guanLiQuanXian: Mapped[Optional[str]] = mapped_column('guanLiQuanXian', String(100))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 chaKanQuanXian 的数据库列类型和约束；本行设置 `chaKanQuanXian: Mapped[Optional[str]] = mapped_column('chaKanQuanXian', String(100))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    chaKanQuanXian: Mapped[Optional[str]] = mapped_column('chaKanQuanXian', String(100))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 shiFouJingZhun 的数据库列类型和约束；本行设置 `shiFouJingZhun: Mapped[Optional[bool]] = mapped_column('shiFouJingZhun', Boolean, server_defaul…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    shiFouJingZhun: Mapped[Optional[bool]] = mapped_column('shiFouJingZhun', Boolean, server_default=text('TRUE'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 shiFouKeKuoZhan 的数据库列类型和约束；本行设置 `shiFouKeKuoZhan: Mapped[Optional[bool]] = mapped_column('shiFouKeKuoZhan', Boolean, server_defa…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    shiFouKeKuoZhan: Mapped[Optional[bool]] = mapped_column('shiFouKeKuoZhan', Boolean, server_default=text('FALSE'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 tscId 的数据库列类型和约束；本行设置 `tscId: Mapped[Optional[str]] = mapped_column('tscId', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    tscId: Mapped[Optional[str]] = mapped_column('tscId', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 zhuangTai 的数据库列类型和约束；本行设置 `zhuangTai: Mapped[Optional[str]] = mapped_column('zhuangTai', String(50), server_default=text("…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    zhuangTai: Mapped[Optional[str]] = mapped_column('zhuangTai', String(50), server_default=text("'启用'"))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 paiXu 的数据库列类型和约束；本行设置 `paiXu: Mapped[Optional[int]] = mapped_column('paiXu', Integer, server_default=text('0'))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    paiXu: Mapped[Optional[int]] = mapped_column('paiXu', Integer, server_default=text('0'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 beiZhu 的数据库列类型和约束；本行设置 `beiZhu: Mapped[Optional[str]] = mapped_column('beiZhu', String(500))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    beiZhu: Mapped[Optional[str]] = mapped_column('beiZhu', String(500))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_flag 的数据库列类型和约束；本行设置 `del_flag: Mapped[Optional[bool]] = mapped_column('del_flag', Boolean, server_default=text('FALS…`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    del_flag: Mapped[Optional[bool]] = mapped_column('del_flag', Boolean, server_default=text('FALSE'))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 del_time 的数据库列类型和约束；本行设置 `del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_userid 的数据库列类型和约束；本行设置 `in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 in_time 的数据库列类型和约束；本行设置 `in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 up_userid 的数据库列类型和约束；本行设置 `up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))
    # [2026-07-03 18:11:51] 作用：定义 ORM 字段 up_time 的数据库列类型和约束；本行设置 `up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)`；理由依据：源模块 extraction_chain.erp_ai_models 仅服务 DeepSeek 提取入库链，按业务边界保留在专属目录；本行位于类 AIZiChanLeiXing
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)
