# -*- coding: utf-8 -*-
from sqlalchemy import (
    BigInteger,
    Integer,
    Column,
    DateTime,
    SmallInteger,
    String,
)
from model import (
    Base
)
from utils.timeformat import get_now_time


class User(Base):
    # 实际数据库的表名
    __tablename__ = "user"

    # 实际数据库的字段，表需要自己写sql建，这里只是将模型类和数据库关联上
    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=64), nullable=False)
    mobile = Column(String(length=11), nullable=False)
    status = Column(SmallInteger, default=1, nullable=False)
    created_at = Column(DateTime, nullable=False, default=get_now_time())

