# -*- coding: utf-8 -*-

# 回复消息的选择器
from apis.FundationApi import Fundation
from apis.TuringRobotApi import getMsgFromTuring
from apis.ZhihuDalyAip import getMsgFromZhihuDaly
from messageI.BackMsg import BackMsg


def getReturnMessage(msg, id):
    if "知乎日报" in msg:
        return getMsgFromZhihuDaly(msg,id)
    elif "基金" in msg:
        fund = Fundation()
        resMsg = fund.startScrapy()
        backMsg = BackMsg(resMsg,id)
        return backMsg
    else:
        return getMsgFromTuring(msg, id)
