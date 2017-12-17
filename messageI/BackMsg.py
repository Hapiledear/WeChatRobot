# -*- coding: utf-8 -*-



import types

# arr是被分割的list，n是每个chunk中含n元素。
def chunks(arr, n):
    return [arr[i:i + n] for i in range(0, len(arr), n)]

class BackMsg(object):
    def __init__(self, msgs, toId):
        self.msgs = msgs
        self.toId = toId

    def onlyOneMsg(self):
        return isinstance(self.msgs, str)

class MsgSendObj(object):

    def __init__(self,nickName,msgs):
        self.nickName = nickName
        self.msgs = msgs