# -*- coding: utf-8 -*-
import logging

from logConfig import setup_logging
from messageI.MessageRouter import getReturnMessage
from wxbot import WXBot

logger = logging.getLogger(__name__)
setup_logging()

procname = "WeChatRobot"

import setproctitle
setproctitle.setproctitle(procname)


class MyWXBot(WXBot):
    def handle_msg_all(self, msg):

        reqMsg = msg['content']['data']

        if isinstance(reqMsg, str) and reqMsg.startswith(r"玄姬，") and msg['content']['type'] == 0:
            msgObj = getReturnMessage(reqMsg, msg['user']['id'])
            if msgObj.onlyOneMsg():
                self.send_msg_by_uid(msgObj.msgs, msg['user']['id'])
            else:
                for resMsg in msgObj.msgs:
                    self.send_msg_by_uid(resMsg, msg['user']['id'])
        return
        # if msg['msg_type_id'] == 4 and msg['content']['type'] == 0:
        #     self.send_msg_by_uid(u'hi', msg['user']['id'])
        #     #self.send_img_msg_by_uid("img/1.png", msg['user']['id'])
        #     #self.send_file_msg_by_uid("img/1.png", msg['user']['id'])
'''
    def schedule(self):
        self.send_msg(u'张三', u'测试')
        time.sleep(1)
'''


def main():
    bot = MyWXBot()
    bot.DEBUG = False
    bot.conf['qr'] = 'tty'
    bot.run()


if __name__ == '__main__':
    main()