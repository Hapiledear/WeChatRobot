# -*- coding: utf-8 -*-
import logging

import itchat

from Shedules import FindationShedule
from apis.AmericanTV import AmericanTVApi
from logConfig import setup_logging
from messageI.MessageRouter import getReturnMessage
from orm.moduls import ChatSubjectFundation

logger = logging.getLogger(__name__)
setup_logging()

procname = "WeChatRobot"

import setproctitle

setproctitle.setproctitle(procname)


def loginSuccessHandle():
    logger.info("登陆成功")
    try:
        FindationShedule.start_apshedule()
    except Exception as e:
        logger.exception(e)


def exitHandle():
    logger.info("exit")
    FindationShedule.stop_apshedule()

# 文件助手走的是这里
@itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
def friendChat(msg):
    logger.debug('%s: %s' % (msg.type, msg.text))
    reqMsg = msg.text
    if isinstance(reqMsg, str) and reqMsg.startswith(r"玄姬，"):
        userName = msg.User.UserName
        if userName == 'filehelper':
            nickName = 'self'
        else:
            nickName = msg.User.NickName
        msgObj = getReturnMessage(reqMsg, msg.FromUserName, nickName)
        if msgObj.onlyOneMsg():
            msg.user.send(msgObj.msgs)
        else:
            for resMsg in msgObj.msgs:
                msg.user.send(resMsg)


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def groupChat(msg):
    logger.debug('%s: %s' % (msg.type, msg.text))
    reqMsg = msg.text
    if isinstance(reqMsg, str) and reqMsg.startswith(r"玄姬，"):
        userName = msg.User.UserName
        if userName == 'filehelper':
            nickName = 'self'
        else:
            nickName = msg.User.NickName
        msgObj = getReturnMessage(reqMsg, msg.FromUserName, nickName)
        if msgObj.onlyOneMsg():
            msg.user.send(msgObj.msgs)
        else:
            for resMsg in msgObj.msgs:
                msg.user.send(resMsg)


# 未知
@itchat.msg_register(itchat.content.TEXT, isMpChat=True)
def mpChat(msg):
    pass


if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2, loginCallback=loginSuccessHandle, exitCallback=exitHandle)
    itchat.run(debug=True)

    # tv = AmericanTVApi("self")
    # tv.scrapyTvInfo("绿箭侠第六季")