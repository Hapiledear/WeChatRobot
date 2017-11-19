# -*- coding: utf-8 -*-
import logging

import itchat

from Shedules import FindationShedule
from logConfig import setup_logging
from messageI.MessageRouter import getReturnMessage

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


@itchat.msg_register(itchat.content.TEXT, isFriendChat=True, isGroupChat=True, isMpChat=True)
def print_content(msg):
    logger.info('%s: %s' % (msg.type, msg.text))
    reqMsg = msg.text
    if isinstance(reqMsg, str) and reqMsg.startswith(r"玄姬，") and msg['content']['type'] == 0:
        msgObj = getReturnMessage(reqMsg, msg['user']['id'])
        if msgObj.onlyOneMsg():
            msg.user.send(msgObj.msgs)
        else:
            for resMsg in msgObj.msgs:
                msg.user.send(resMsg)


if __name__ == '__main__':
    itchat.auto_login(enableCmdQR=2, loginCallback=loginSuccessHandle, exitCallback=exitHandle)
    itchat.run(debug=True)
