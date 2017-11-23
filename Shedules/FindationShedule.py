# -*- coding: utf-8 -*-
import logging

import itchat
from pytz import utc

from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

from apis.FundationApi import Fundation

LOGGER = logging.getLogger(__name__)
#
# jobstores = {
#     'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
# }
# executors = {
#     'default': ThreadPoolExecutor(20),
#     'processpool': ProcessPoolExecutor(5)
# }
# job_defaults = {
#     'coalesce': False,
#     'max_instances': 3
# }

_schedual = ""


def start_apshedule():
    targets = itchat.search_chatrooms(name='奔小康')
    userNames = []
    if targets:
        for target in targets:
            userNames.append(target.UserName)
    else:
        LOGGER.warning("未找到相关群聊，请检查是否变更了群名称")

    sched = BackgroundScheduler(daemonic=False)
    sched._logger = LOGGER
    sched.add_job(func=scrapAndSenFinMsg, args=[userNames], replace_existing=True, misfire_grace_time=3,
                  trigger='cron', name='基金查询_预估值', id='scrap_fin', minute='0,15,30,45', hour='9-14', day_of_week='0-4')
    sched.add_job(func=scrapAndSenFinAccMsg, args=[userNames], replace_existing=True, misfire_grace_time=3,
                  trigger='cron', name='基金查询_实际值', id='scrap_fin_acc', minute='1', hour='22', day_of_week='0-4')
    sched.start()
    global _schedual
    _schedual = sched


def stop_apshedule():
    _schedual.shutdown()


def scrapAndSenFinMsg(userNames):
    LOGGER.info("开始执行基金查询任务")
    fund = Fundation()
    resMsg = fund.startScrapy(type=1)
    LOGGER.debug(resMsg)
    for userName in userNames:
        itchat.send_msg(resMsg, toUserName=userName)


def scrapAndSenFinAccMsg(userNames):
    LOGGER.info("开始执行基金查询任务")
    fund = Fundation()
    resMsg = fund.startScrapy(type=2)
    LOGGER.debug(resMsg)
    for userName in userNames:
        itchat.send_msg(resMsg, toUserName=userName)
