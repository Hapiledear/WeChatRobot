# -*- coding: utf-8 -*-
import logging

import time
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import sessionmaker

from apis.AmericanTV import AmericanTVApi
from messageI.BackMsg import MsgSendObj
from messageI.MessageRouter import sendMsgByMsgSendObj
from orm.moduls import engine, AmericanTV, ChatSubAmercanTv, AmericanTVSets

LOGGER = logging.getLogger(__name__)

_schedual = ""


def start_apshedule():
    nickNames = ['奔小康']

    sched = BackgroundScheduler(daemonic=False)
    sched._logger = LOGGER
    sched.add_job(func=scrapAmericanTv, replace_existing=True, misfire_grace_time=3,
                  trigger='cron', name='美剧更新查看', id='scrap_american_tv', minute='0', hour='20')

    sched.add_job(func=resetUpdState, replace_existing=True, misfire_grace_time=3,
                  trigger='cron', name='美剧——将已推送变为未更新', id='scrap_american_tv', minute='0', hour='0')
    #
    # sched.add_job(func=scrapAndSenFinMsg, args=[nickNames], replace_existing=True, misfire_grace_time=3,
    #               trigger='cron', name='基金查询_测试', id='scrap_fin_test', minute='0/2')
    sched.start()
    global _schedual
    _schedual = sched


def stop_apshedule():
    _schedual.shutdown()


def resetUpdState():
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        session.query(ChatSubAmercanTv).filter(
            ChatSubAmercanTv.have_updated == "2").update(
            {ChatSubAmercanTv.have_updated: "0"})
    finally:
        session.commit()
        session.close()


def scrapAmericanTv():
    n_dayOfWeek = time.localtime(time.time())[6] - 1
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        # 爬取当日的更新数据
        today_american_tv_sets = session.query(AmericanTV).filter(
            AmericanTV.send_week == n_dayOfWeek).all()
        for tv in today_american_tv_sets:
            aTvApi = AmericanTVApi()
            updateTv_Sets = aTvApi.startScripyByTTCode(tv.tiantian_code, tv.u_id)
            if updateTv_Sets:
                session.query(ChatSubAmercanTv).filter(
                    ChatSubAmercanTv.american_tv == tv.u_id).update(
                    {ChatSubAmercanTv.have_updated: "1", ChatSubAmercanTv.new_set_id: updateTv_Sets[-1]})
        # 向每个订阅者进行推送
        sendUpdAmercanTv(session)
    finally:
        session.commit()
        session.close()


def sendUpdAmercanTv(session):
    sendList = session.query(ChatSubAmercanTv).filter(ChatSubAmercanTv.have_updated == "1").all()
    for target in sendList:
        setsInfo = session.query(AmericanTVSets).filter(AmericanTVSets.u_id == target.new_set_id).first()
        msg = "您订阅的美剧更新了:\n{0} 第{1}集 链接 {2}"
        msg = msg.format(target.tv_name, setsInfo.set_ordinal, setsInfo.baidu_cloud_url)
        sendMsg = MsgSendObj(target.chat_name, msg)
        # sendMsgByMsgSendObj(sendMsg)
        session.query(ChatSubAmercanTv).filter(
            ChatSubAmercanTv.u_id == target.u_id).update(
            {ChatSubAmercanTv.have_updated: "2"})

if __name__ == '__main__':
    scrapAmericanTv()