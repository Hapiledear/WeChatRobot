# -*- coding: utf-8 -*-
import logging
import re

import requests

from orm.moduls import FundationObject

LOGGER = logging.getLogger(__name__)

re_stock_code = r'(?<=\.com\/).*(?=\.html)'


class Fundation(object):
    session = requests.Session()
    header_info = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    session.headers.update(header_info)
    start_url = "http://fund.eastmoney.com/{0}.html?spm=search"

    fundCodes = ['001426', '202005', '004450', '040015', '001986', '159916', '162213', '340007', '040008', '002851',
                 '050002', '161725', '340008', '001616', '002984', '001542']

    def startScrapy(self):
        resMsg = "每日基金定时播报(估算):\n"
        fundObjList = []
        for fundCode in self.fundCodes:
            reqUrl = self.start_url.format(fundCode)
            response = self.session.get(reqUrl)  # get请求方式，并设置请求头
            fundObj = self.parseResponse(response, fundCode)
            fundObjList.append(fundObj)

        sorted_list =  sorted(fundObjList, key=lambda fund: fund.predict_grow_int)
        for fundObj in sorted_list:
            resMsg = resMsg + fundObj.fun_name + ":" + fundObj.predict_grow + "\n"
        return resMsg

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
        fundObj.predict_grow = predict_grow
        fundObj.predict_grow_int = percent_to_int(predict_grow)

        stockHtml = html.xpath('//*[@id="position_shares"]/div[1]/table/tr')
        for stock in stockHtml[1:]:
            s_code_herf = stock.xpath('td[1]/a')[0].attrib['href']
            s_code = re.findall(re_stock_code, s_code_herf)[0]
            s_name = stock.xpath('td[1]/a')[0].text
            s_weight = stock.xpath('td[2]')[0].text
            s_grow = stock.xpath('td[3]/span')[0].text
            LOGGER.debug(s_name)

        return fundObj


def percent_to_int(string):
    if "%" in string:
        newint = float(string.strip("%"))
        return newint
    else:
        LOGGER.info("你输入的不是百分比！")


# if __name__ == '__main__':
#     fund = Fundation()
#     resMsg = fund.startScrapy()