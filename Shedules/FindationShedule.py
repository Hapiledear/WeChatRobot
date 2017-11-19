# -*- coding: utf-8 -*-
import logging

import itchat
from pytz import utc

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

LOGGER = logging.getLogger(__name__)


def start_apshedule():
    targets = itchat.search_chatrooms(name='停车做爱枫林晚')
    userNames = []
    if targets:
        for target in targets:
            userNames.append(target.UserName)
    else:
        LOGGER.warning("未找到相关群聊，请检查是否变更了群名称")

    sched = BackgroundScheduler()
    sched.add_job(func=scrapAndSenFinMsg, args=[userNames],trigger='cron', name='基金查询', id='scrap_fin', minute='0/1')
    sched.start()


def scrapAndSenFinMsg(userNames):
    LOGGER.info("开始执行基金查询任务")
    for userName in userNames:
        itchat.send_msg("车车车!", toUserName=userName)
