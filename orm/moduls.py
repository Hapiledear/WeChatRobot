# -*- coding: utf-8 -*-

# 设置INSTALLED_APPS信息
import sqlalchemy
from datetime import date
from sqlalchemy import *

from sqlalchemy.ext.declarative import declarative_base

# 设置数据库信息
mysql_test = "mysql+pymysql://yanghuang:19951015@172.16.20.55:3306/wcr?charset=utf8"
mysql_conn = "mysql+pymysql://yanghuang:19951015@47.96.30.206:3306/wcr?charset=utf8"

engine = create_engine(mysql_conn, max_overflow=5)
# 生成一个SqlORM 基类
Base = declarative_base()


# 构造ORM的
class FundationObject(Base):
    __tablename__ = 'fundation'
    id = Column(Integer,primary_key=True, autoincrement='ignore_fk')
    fun_code = Column(String(10))
    fun_name = Column(String(100))
    acc_grow = Column(String(10))
    acc_grow_int = Column(Integer)
    predict_grow = Column(String(10))
    predict_grow_int = Column(INTEGER)
    date = Column('t_date', String(8))


class ChatSubjectFundation(Base):
    __tablename__ = 'chat_sub_fun'
    u_id = Column(String(36), primary_key=True)
    chat_name = Column(String(100))
    target_code = Column(String(10))
    target_name = Column(String(100))
    del_flag = Column(Boolean)
    send_type = Column(String(1), server_default='1')
