# [2026-07-03 14:26:28] 中文迁移说明：本文件完整复制自 app/models/erp_ai_models.py；纳入依据为 DeepSeek 提取入库链 的项目内传递依赖闭包。
from typing import Optional
import datetime
import decimal

from sqlalchemy import (
    BigInteger,
    Boolean,
    DateTime,
    DECIMAL,
    Integer,
    PrimaryKeyConstraint,
    SmallInteger,
    String,
    Text,
    text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


# This file is generated from erp???1_postgresql_create_tables.sql.
# Keep mapped_column("...") names aligned with PostgreSQL quoted column names.

class ErpWendaJilu(Base):
    __tablename__ = "AI_Wendajilu"
    __table_args__ = (
        PrimaryKeyConstraint('wdjl_ id', 'Yssj_id', name="pk_AI_Wendajilu"),
        {"comment": "Generated ORM for AI_Wendajilu"},
    )

    wdjl_id: Mapped[int] = mapped_column('wdjl_ id', String(64), primary_key=True, autoincrement=False, nullable=False)
    Yssj_id: Mapped[int] = mapped_column('Yssj_id', String(64), primary_key=True, autoincrement=False, nullable=False)
    AI_WenTi: Mapped[Optional[str]] = mapped_column('AI_WenTi', Text)
    AI_DaAn: Mapped[Optional[str]] = mapped_column('AI_DaAn', Text)
    AI_Biaozhu: Mapped[Optional[str]] = mapped_column('AI_Biaozhu', Text)
    WenTiYuanWen: Mapped[Optional[str]] = mapped_column('WenTiYuanWen', Text)
    DaAnYuanWen: Mapped[Optional[str]] = mapped_column('DaAnYuanWen', Text)
    WenTi_true: Mapped[Optional[str]] = mapped_column('WenTi_true', Text)
    DaAn_true: Mapped[Optional[str]] = mapped_column('DaAn_true', Text)
    Biaozhu_true: Mapped[Optional[str]] = mapped_column('Biaozhu_true', Text)
    ZhuangTai: Mapped[Optional[int]] = mapped_column('ZhuangTai', Integer)
    ZhuangTai_id: Mapped[Optional[int]] = mapped_column('ZhuangTai_id', Integer)
    ZhuangTai_time: Mapped[Optional[datetime.datetime]] = mapped_column('ZhuangTai_time', DateTime)
    YinPinShiJian: Mapped[Optional[str]] = mapped_column('YinPinShiJian', DateTime)
    gsId: Mapped[Optional[int]] = mapped_column('gsId', String(64))
    in_userid: Mapped[Optional[int]] = mapped_column('in_userid', String(64))
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)


class ErpYitu(Base):
    __tablename__ = "AI_Yitu"
    __table_args__ = (
        PrimaryKeyConstraint('yt_ id', 'Yssj_id', name="pk_AI_Yitu"),
        {"comment": "Generated ORM for AI_Yitu"},
    )

    yt_id: Mapped[int] = mapped_column('yt_ id', String(64), primary_key=True, autoincrement=False, nullable=False)
    Yssj_id: Mapped[int] = mapped_column('Yssj_id', String(64), primary_key=True, autoincrement=False, nullable=False)
    AI_YiTu: Mapped[Optional[str]] = mapped_column('AI_YiTu', Text)
    YiTu: Mapped[Optional[str]] = mapped_column('YiTu', Text)
    BiaoZhu: Mapped[Optional[str]] = mapped_column('BiaoZhu', Text)
    ZhuangTai: Mapped[Optional[int]] = mapped_column('ZhuangTai', Integer)
    ZhuangTai_id: Mapped[Optional[int]] = mapped_column('ZhuangTai_id', Integer)
    ZhuangTai_time: Mapped[Optional[datetime.datetime]] = mapped_column('ZhuangTai_time', DateTime)
    ShiJian: Mapped[Optional[str]] = mapped_column('ShiJian', String(255))
    gsId: Mapped[Optional[int]] = mapped_column('gsId', String(64))
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    in_userid: Mapped[Optional[int]] = mapped_column('in_userid', String(64))
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)


class ErpYuanShiShuJu(Base):
    __tablename__ = "AI_YuanShishuju"
    __table_args__ = (
        PrimaryKeyConstraint('shuju_id', 'GuanLianKeHu', name="pk_AI_YuanShishuju"),
        {"comment": "Generated ORM for AI_YuanShishuju"},
    )

    shuju_id: Mapped[str] = mapped_column('shuju_id', String(64), primary_key=True, autoincrement=False, nullable=False)
    ZcLeiXin: Mapped[Optional[str]] = mapped_column('ZcLeiXin', String(64))
    ShuJu: Mapped[Optional[str]] = mapped_column('ShuJu', Text)
    WenJianDiZhi: Mapped[Optional[str]] = mapped_column('WenJianDiZhi', Text)
    WenJianName: Mapped[Optional[str]] = mapped_column('WenJianName', Text)
    LaiYuan: Mapped[Optional[int]] = mapped_column('LaiYuan', Integer)
    GuanLianKeHu: Mapped[int] = mapped_column('GuanLianKeHu', Integer, primary_key=True, autoincrement=False, nullable=False)
    gs_id: Mapped[Optional[str]] = mapped_column('gs_id', Integer)
    del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False, server_default=text('FALSE'))
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
    up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)


class ErpGongSi(Base):
    __tablename__ = "AI_GongSi"
    __table_args__ = (
        PrimaryKeyConstraint('gsId', name="pk_AI_GongSi"),
        {"comment": "Generated ORM for AI_GongSi"},
    )

    gsId: Mapped[str] = mapped_column('gsId',String(64), primary_key=True, autoincrement=False, nullable=False)
    gongSiDaiMa: Mapped[Optional[str]] = mapped_column('gongSiDaiMa', String(255))
    gongSiQuanCheng: Mapped[Optional[str]] = mapped_column('gongSiQuanCheng', String(255))
    gongSiJianCheng: Mapped[Optional[str]] = mapped_column('gongSiJianCheng', String(50))
    gongSiDiZhi: Mapped[Optional[str]] = mapped_column('gongSiDiZhi', String(255))
    del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False, server_default=text('FALSE'))
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
    up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)


class AILiaoTianZhu(Base):
    __tablename__ = "AI_liaotianzhu"
    __table_args__ = (
        PrimaryKeyConstraint('Ltz_id', name="pk_AI_liaotianzhu"),
        {"comment": "Generated ORM for AI_liaotianzhu"},
    )

    Ltz_id: Mapped[str] = mapped_column('Ltz_id', String(64), primary_key=True, autoincrement=False, nullable=False)
    session_id: Mapped[str] = mapped_column('session_id', String(64), nullable=False)
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column('create_at', DateTime, server_default=text('CURRENT_TIMESTAMP'))
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False)
    gsyh_id: Mapped[str] = mapped_column('gsyh_id', String(64), nullable=False)
    gs_id: Mapped[str] = mapped_column('gs_id', String(64), nullable=False)
    title: Mapped[Optional[str]] = mapped_column('title', String(255))


class AILiaoTianJiLu(Base):
    __tablename__ = "AI_liaotianjilu"
    __table_args__ = (
        PrimaryKeyConstraint("ltjlid", name="pk_AI_liaotianjilu"),
        {"comment": "Generated ORM for AI_liaotianjilu"},
    )

    ltjlid: Mapped[str] = mapped_column("ltjlid", String(64), primary_key=True, autoincrement=False, nullable=False)
    ltz_id: Mapped[str] = mapped_column("ltz_id", String(64), nullable=False, index=True)

    message_role: Mapped[str] = mapped_column("message_role", String(10), nullable=False)
    message_content: Mapped[str] = mapped_column("message_content", Text, nullable=False)
    Moshi: Mapped[Optional[int]] = mapped_column("Moshi", Integer)
    Wenjian_id: Mapped[Optional[str]] = mapped_column("Wenjian_id", String(64))
    PingJia: Mapped[Optional[str]] = mapped_column("PingJia", String(255))
    create_at: Mapped[Optional[datetime.datetime]] = mapped_column("create_at", DateTime, server_default=text("CURRENT_TIMESTAMP"))
    gx_create_at: Mapped[Optional[datetime.datetime]] = mapped_column("gx_create_at", DateTime)
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column("del_time", DateTime)
    del_flag: Mapped[bool] = mapped_column("del_flag", Boolean, nullable=False)


class AIGongSiYongHu(Base):
    __tablename__ = "AI_GongSiYongHu"
    __table_args__ = (
        PrimaryKeyConstraint('gsyhId', name="pk_AI_GongSiYongHu"),
        {"comment": "Generated ORM for AI_GongSiYongHu"},
    )

    gsyhId: Mapped[str] = mapped_column('gsyhId', String(64), primary_key=True, autoincrement=False, nullable=False)
    yongHuXingMing: Mapped[Optional[str]] = mapped_column('yongHuXingMing', String(255))
    xingBie: Mapped[Optional[int]] = mapped_column('xingBie', SmallInteger, server_default=text('0'))
    dianHua: Mapped[Optional[str]] = mapped_column('dianHua', String(11))
    gsId: Mapped[Optional[str]] = mapped_column('gsId', String(64))
    del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False, server_default=text('FALSE'))
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
    up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)


class AIYongHuShiYongTongJi(Base):
    __tablename__ = "AI_YongHuShiYongTongJi"
    __table_args__ = (
        PrimaryKeyConstraint('syjlId', name="pk_AI_YongHuShiYongTongJi"),
        {"comment": "Generated ORM for AI_YongHuShiYongTongJi"},
    )

    syjlId: Mapped[str] = mapped_column('syjlId', String(64), primary_key=True, autoincrement=False, nullable=False)
    yongHuId: Mapped[Optional[str]] = mapped_column('yongHuId', String(64))
    gsId: Mapped[str] = mapped_column('gsId', BigInteger, nullable=False)
    buMenId: Mapped[Optional[int]] = mapped_column('buMenId', BigInteger)
    session_id: Mapped[Optional[str]] = mapped_column('session_id', String(64))
    ai_gongNeng: Mapped[Optional[str]] = mapped_column('ai_gongNeng', String(100))
    yeWuChangJing: Mapped[Optional[str]] = mapped_column('yeWuChangJing', String(100))
    wenTiLeiXing: Mapped[Optional[str]] = mapped_column('wenTiLeiXing', String(100))
    tiWenNeiRong: Mapped[Optional[str]] = mapped_column('tiWenNeiRong', Text)
    aiHuiDaNeiRong: Mapped[Optional[str]] = mapped_column('aiHuiDaNeiRong', Text)
    shiFouCaiNa: Mapped[Optional[bool]] = mapped_column('shiFouCaiNa', Boolean, server_default=text('FALSE'))
    caiNaFangShi: Mapped[Optional[str]] = mapped_column('caiNaFangShi', String(50))
    qingQiuToken: Mapped[Optional[int]] = mapped_column('qingQiuToken', Integer)
    huiDaToken: Mapped[Optional[int]] = mapped_column('huiDaToken', Integer)
    feiYong: Mapped[Optional[decimal.Decimal]] = mapped_column('feiYong', DECIMAL(18, 6))
    shiYongShiJian: Mapped[datetime.datetime] = mapped_column('shiYongShiJian', DateTime, nullable=False)
    del_flag: Mapped[Optional[bool]] = mapped_column('del_flag', Boolean, server_default=text('FALSE'))
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
    up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)


class AITiShiCiGuanLiBiao(Base):
    __tablename__ = "AI_erp_TiShiCiGuanLiBiao"
    __table_args__ = (
        PrimaryKeyConstraint('tscId', name="pk_AI_erp_TiShiCiGuanLiBiao"),
        {"comment": "Generated ORM for AI_erp_TiShiCiGuanLiBiao"},
    )

    tscId: Mapped[str] = mapped_column('tscId', String(64), primary_key=True, autoincrement=False, nullable=False)
    systemPrompt: Mapped[Optional[str]] = mapped_column('systemPrompt', Text)
    UsermPrompt: Mapped[str] = mapped_column('UsermPrompt', Text, nullable=False)
    ShuChuGeShi: Mapped[Optional[str]] = mapped_column('ShuChuGeShi', Text)
    tiShiCiBianMa: Mapped[str] = mapped_column('tiShiCiBianMa', String(100), nullable=False)
    TiShiCiZhuangTai: Mapped[Optional[int]] = mapped_column('TiShiCiZhuangTai', Integer)
    Tishicileixing: Mapped[Optional[int]] = mapped_column('Tishicileixing', Integer)
    gsId: Mapped[Optional[str]] = mapped_column('gsId', String(64))
    del_flag: Mapped[bool] = mapped_column('del_flag', Boolean, nullable=False, server_default=text('FALSE'))
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
    up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)


class AIZiChanLeiXing(Base):
    __tablename__ = "AI_ZiChanLeiXing"
    __table_args__ = (
        PrimaryKeyConstraint('zclxId', name="pk_AI_ZiChanLeiXing"),
        {"comment": "Generated ORM for AI_ZiChanLeiXing"},
    )

    zclxId: Mapped[str] = mapped_column('zclxId', String(64), primary_key=True, autoincrement=False, nullable=False)
    gsId: Mapped[str] = mapped_column('gsId', String(64), nullable=False)
    ziChanLeiXing: Mapped[str] = mapped_column('ziChanLeiXing', String(100), nullable=False)
    ziChanShuoMing: Mapped[Optional[str]] = mapped_column('ziChanShuoMing', String(500))
    zhiShiShuLiang: Mapped[Optional[int]] = mapped_column('zhiShiShuLiang', Integer, server_default=text('0'))
    guanLiQuanXian: Mapped[Optional[str]] = mapped_column('guanLiQuanXian', String(100))
    chaKanQuanXian: Mapped[Optional[str]] = mapped_column('chaKanQuanXian', String(100))
    shiFouJingZhun: Mapped[Optional[bool]] = mapped_column('shiFouJingZhun', Boolean, server_default=text('TRUE'))
    shiFouKeKuoZhan: Mapped[Optional[bool]] = mapped_column('shiFouKeKuoZhan', Boolean, server_default=text('FALSE'))
    tscId: Mapped[Optional[str]] = mapped_column('tscId', String(64))
    zhuangTai: Mapped[Optional[str]] = mapped_column('zhuangTai', String(50), server_default=text("'启用'"))
    paiXu: Mapped[Optional[int]] = mapped_column('paiXu', Integer, server_default=text('0'))
    beiZhu: Mapped[Optional[str]] = mapped_column('beiZhu', String(500))
    del_flag: Mapped[Optional[bool]] = mapped_column('del_flag', Boolean, server_default=text('FALSE'))
    del_time: Mapped[Optional[datetime.datetime]] = mapped_column('del_time', DateTime)
    in_userid: Mapped[Optional[str]] = mapped_column('in_userid', String(64))
    in_time: Mapped[Optional[datetime.datetime]] = mapped_column('in_time', DateTime)
    up_userid: Mapped[Optional[str]] = mapped_column('up_userid', String(64))
    up_time: Mapped[Optional[datetime.datetime]] = mapped_column('up_time', DateTime)
