# -*- coding: utf-8 -*-

# 回复消息的选择器
from apis.TuringRobotApi import getMsgFromTuring
from apis.ZhihuDalyAip import getMsgFromZhihuDaly


def getReturnMessage(msg, id):
    if "知乎日报" in msg:
        return getMsgFromZhihuDaly(msg,id)
    else:
        return getMsgFromTuring(msg, id)
