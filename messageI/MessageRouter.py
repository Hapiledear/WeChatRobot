# -*- coding: utf-8 -*-

# 回复消息的选择器
import logging

import itchat
from apis.FundationApi import Fundation
from apis.TuringRobotApi import getMsgFromTuring
from apis.ZhihuDalyAip import getMsgFromZhihuDaly
from messageI.BackMsg import BackMsg

LOGGER = logging.getLogger(__name__)


def getReturnMessage(msg, id, userName):
    if "知乎日报" in msg:
        return getMsgFromZhihuDaly(msg, id)
    elif "基金" in msg:
        fund = Fundation([userName])
        resMsg = fund.startScrapy(type=0)
        backMsg = BackMsg(resMsg, id)
        return backMsg
    else:
        return getMsgFromTuring(msg, id)


def sendMsgByNickNames(resMsg, nickNames):
    targets = []
    if nickNames:
        for nickName in nickNames:
            ls = itchat.search_chatrooms(name=nickName)
            if len(ls) == 1:
                targets.append(ls[0])
            elif len(ls) > 1:
                LOGGER.info("%s 找到多个群，只取第一个%s" % (nickName, ls))
                targets.append(ls[0])
    userNames = []
    if targets:
        for target in targets:
            userNames.append(target.UserName)
    else:
        LOGGER.warning("未找到相关群聊，请检查是否变更了群名称")
    for userName in userNames:
        itchat.send_msg(resMsg, toUserName=userName)
