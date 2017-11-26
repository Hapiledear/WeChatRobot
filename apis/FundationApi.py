# -*- coding: utf-8 -*-
import json
import logging
import re

import requests
import time

from datetime import date

from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

from orm.moduls import FundationObject, engine, ChatSubjectFundation

LOGGER = logging.getLogger(__name__)

re_stock_code = r'(?<=\.com\/).*(?=\.html)'
re_get_json = r'{.*}'


class Fundation(object):
    # 类中属性为类的所有实例共有
    session = requests.Session()
    header_info = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    session.headers.update(header_info)
    start_url = "http://fund.eastmoney.com/{0}.html?spm=search"
    fund_pred_url = "http://fundgz.1234567.com.cn/js/{0}.js?rt={1}"

    # self.XXX的属性为单个实例独有
    def __init__(self, userNames):
        from orm.moduls import ChatSubjectFundation
        self.userNames = userNames
        self.fundCodes_from_db = []

        Session = sessionmaker(bind=engine)
        session = Session()
        subjectFundObjs = session.query(ChatSubjectFundation).filter(
            ChatSubjectFundation.chat_name.in_(self.userNames)).all()
        for t in subjectFundObjs:
            self.fundCodes_from_db.append(t.target_code)
        session.commit()
        session.close()

    fundCodes = ['001426', '202005', '004450', '159916', '162213', '340007', '040008', '002851',
                 '050002', '161725', '340008', '001616', '002984', '001542', '020026']

    def startScrapy(self, type):
        resMsg = "每日基金定时播报(估算):\n"
        resMsg2 = "今日基金实际涨势:\n"
        print("%s 的基金订阅:%s" % (self.userNames, self.fundCodes_from_db))
        if len(self.fundCodes_from_db) == 0:
            return "暂无基金订阅"

        n_dayOfWeek = time.localtime(time.time())[6]
        n_hour = time.localtime(time.time())[3]

        if type == 0:
            if int(n_hour) >= 22:
                type = 2
            else:
                type = 1

        if type == 1:
            fun_predict_list = self.getFunPredInfo()
            self.saveFundInfo(fun_predict_list)
            for fundObj in fun_predict_list:
                resMsg = resMsg + fundObj.fun_name + ":" + fundObj.predict_grow + "\n"
            return resMsg
        else:
            fun_acc_list = self.getFunAccInfo()
            self.saveFundInfo(fun_acc_list)
            for fundObj in fun_acc_list:
                resMsg2 = resMsg2 + fundObj.fun_name + ":" + fundObj.acc_grow + "\n"
            return resMsg2

    def getFunPredInfo(self):
        f_list = []
        for fundCode in self.fundCodes_from_db:
            reqUrl = self.fund_pred_url.format(fundCode, time.time())
            LOGGER.debug("请求url=%s " % reqUrl)
            response = self.session.get(reqUrl)  # get请求方式，并设置请求头
            resJsonStr = re.findall(re_get_json, response.text)[0]
            resJson = json.loads(resJsonStr)

            fundObj = FundationObject()
            fundObj.fun_code = resJson['fundcode']
            fundObj.fun_name = resJson['name']
            fundObj.predict_grow = resJson['gszzl'] + "%"
            fundObj.predict_grow_int = resJson['gszzl']
            fundObj.date = date.today().strftime('%Y-%m-%d')
            f_list.append(fundObj)
        sorted_list = sorted(f_list, key=lambda fund: fund.predict_grow_int)
        return sorted_list

    def getFunAccInfo(self):
        f_list = []
        for fundCode in self.fundCodes_from_db:
            reqUrl = self.start_url.format(fundCode)
            LOGGER.debug("请求url=%s " % reqUrl)
            response = self.session.get(reqUrl)  # get请求方式，并设置请求头
            fundObj = self.parseResponse(response, fundCode)
            f_list.append(fundObj)
        sorted_list_acc = sorted(f_list, key=lambda fund: fund.acc_grow_int)
        return sorted_list_acc

    def parseResponse(self, response, fundCode='0000'):
        htmltext = response.text.encode(response.encoding).decode('utf-8')
        from lxml import etree
        html = etree.HTML(htmltext)
        fundName = html.xpath('//*[@id="body"]/div[9]/div/div/a[3]')[0].text
        acc_grow = html.xpath('//*[@id="body"]/div[12]/div/div/div[2]/div[1]/div[1]/dl[2]/dd[1]/span[2]')[0].text
        predict_grow = html.xpath('//*[@id="gz_gszzl"]')[0].text
        LOGGER.info("基金名称 %s " % fundName)

        fundObj = FundationObject()
        fundObj.fun_code = fundCode
        fundObj.fun_name = fundName
        fundObj.acc_grow = acc_grow
        fundObj.acc_grow_int = percent_to_int(acc_grow)
        fundObj.predict_grow = predict_grow
        fundObj.predict_grow_int = percent_to_int(predict_grow)
        fundObj.date = date.today().strftime('%Y-%m-%d')

        return fundObj

    def saveFundInfo(self, funds):
        if isinstance(funds,list) and funds:
            Session = sessionmaker(bind=engine)
            session = Session()
            try:
                for fund in funds:
                    if isinstance(fund, FundationObject):
                        res = session.query(FundationObject).filter(
                            and_(FundationObject.fun_code == fund.fun_code, FundationObject.date == fund.date)).first()
                        if res is not None:
                            fund.id = res.id
                        session.merge(fund)
                    else:
                        LOGGER.warning("%s 不是FundationObject" % fund.__dict__)
            finally:
                session.commit()
                session.close()


def percent_to_int(string):
    if "%" in string:
        newint = float(string.strip("%"))
        return newint
    else:
        LOGGER.info("你输入的不是百分比！")
