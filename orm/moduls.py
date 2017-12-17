# -*- coding: utf-8 -*-

# 设置INSTALLED_APPS信息
import sqlalchemy
from datetime import date, datetime
from sqlalchemy import *

from sqlalchemy.ext.declarative import declarative_base

# 设置数据库信息
mysql_test = "mysql+pymysql://yanghuang:19951015@172.16.20.55:3306/wcr?charset=utf8"
mysql_conn = "mysql+pymysql://yanghuang:19951015@47.96.30.206:3306/wcr?charset=utf8"

engine = create_engine(mysql_conn, max_overflow=10, pool_size=5, pool_recycle=360)
# 生成一个SqlORM 基类
Base = declarative_base()


# 构造ORM的
class FundationObject(Base):
    __tablename__ = 'fundation'
    id = Column(Integer, primary_key=True, autoincrement='ignore_fk')
    fun_code = Column(String(10))
    fun_name = Column(String(100))
    acc_grow = Column(String(10))
    acc_grow_int = Column(FLOAT)
    predict_grow = Column(String(10))
    predict_grow_int = Column(FLOAT)
    date = Column('t_date', String(8))


class ChatSubjectFundation(Base):
    __tablename__ = 'chat_sub_fun'
    u_id = Column(String(36), primary_key=True)
    chat_name = Column(String(100))
    target_code = Column(String(10))
    target_name = Column(String(100))
    del_flag = Column(Boolean)
    send_type = Column(String(1), server_default='1')


class AmericanTV(Base):
    __tablename__ = 'tv_american'
    u_id = Column(String(36), primary_key=True)
    tv_name = Column(String(100))
    douban_rate = Column(FLOAT)
    douban_code = Column(String(10))
    tiantian_code = Column(String(10))
    send_date = Column(DATE)
    send_week = Column(String(1))
    state = Column(String(1))
    story_type = Column(String(100))


    def setSendDateAndWeek(self,dateWeekly):
        ls = dateWeekly.split()
        dateStr = ls[0].split("：")[1]
        date_time = datetime.strptime(dateStr, '%Y-%m-%d')
        self.send_date = date_time
        weekStr = ls[1]
        if "周六" in weekStr:
            self.send_week = '5'
        elif "周日" in weekStr:
            self.send_week = '6'
        elif "周一" in weekStr:
            self.send_week = '0'
        elif "周二" in weekStr:
            self.send_week = '1'
        elif "周三" in weekStr:
            self.send_week = '2'
        elif "周四" in weekStr:
            self.send_week = '3'
        elif "周五" in weekStr:
            self.send_week = '4'
        else:
            self.send_week = '6'

    def setIntState(self, cState):
        if "状态：连载中" == cState:
            self.state = '1'
        else:
            self.state = '0'


class AmericanTVSets(Base):
    __tablename__ = 'tv_sets_american'
    u_id = Column(String(36), primary_key=True)
    p_id = Column(String(36), ForeignKey('tv_american.u_id'))
    set_ordinal = Column(Integer)
    baidu_cloud_url = Column(String(100))
    magnet_url = Column(String(1000))
    ed2k_url = Column(String(1000))


class ChatSubAmercanTv(Base):
    __tablename__ = 'chat_sub_amerTv'
    u_id = Column(String(36), primary_key=True)
    chat_name = Column(String(100))
    american_tv = Column(String(36))
    tv_name = Column(String(200))
    have_updated = Column(String(1))
    new_set_id = Column(String(36))

