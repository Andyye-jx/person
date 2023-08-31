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
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True)
    name = Column(String(length=64), nullable=False)
    mobile = Column(String(length=11), nullable=False)
    status = Column(SmallInteger, default=1, nullable=False)
    created_at = Column(DateTime, nullable=False, default=get_now_time())

