# -*- coding: utf-8 -*-
import json
import logging
import re
import uuid

import requests

from orm.moduls import AmericanTV, AmericanTVSets

LOGGER = logging.getLogger(__name__)
re_tiantian_code = r'\w+(?=\.html)'


class AmericanTVApi(object):
    session = requests.Session()
    header_info = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

    session.headers.update(header_info)
    url_tiantian_search = "http://www.meijuhui.net/search.php?q={0}"
    url_tiantian_detail = "http://www.meijuhui.net/archives/{0}.html"
    url_douban_search = "https://movie.douban.com/j/subject_suggest?q={0}"

    def __init__(self, userName):
        self.userName = userName

    def startScrapy(self, type=1):
        resMsg = ""

        return resMsg

    def scrapyTvInfo(self, tvName):

        aTv = AmericanTV()
        aTv.u_id = uuid.uuid1()
        # 豆瓣相关信息
        reqUrl = self.url_douban_search.format(tvName)
        LOGGER.debug("请求url=%s " % reqUrl)
        response = self.session.get(reqUrl)  # get请求方式，并设置请求头
        resJson = json.loads(response.text)
        if resJson:
            aTv.douban_code = resJson[0]['id']
            aTv.tv_name = resJson[0]['title']
            # 评分和放送状态由另一定时任务统一抓取后赋值更新
        else:
            LOGGER.info("豆瓣中未找到相关信息，请重新编写关键字")

        # 天天美剧相关信息
        reqUrl = self.url_tiantian_search.format(tvName)
        LOGGER.debug("请求url=%s " % reqUrl)
        response = self.session.get(reqUrl)  # get请求方式，并设置请求头
        htmltext = response.text.encode(response.encoding).decode('utf-8')
        from lxml import etree
        html = etree.HTML(htmltext)
        findList = html.xpath('/html/body/section/div[2]/div/article')
        if findList:
            article = findList[0]
            herf = article.xpath('./div/a')[0].attrib['href']
            code = re.findall(re_tiantian_code, herf)[0]
            aTv.tiantian_code = code
        else:
            LOGGER.info("未找到相关信息，请重新编写关键字")

        # 天天美剧详细信息
        reqUrl = self.url_tiantian_detail.format(aTv.tiantian_code)
        LOGGER.debug("请求url=%s " % reqUrl)
        response = self.session.get(reqUrl)  # get请求方式，并设置请求头
        htmltext = response.text.encode(response.encoding).decode('utf-8')

        html = etree.HTML(htmltext)
        tv_p_list = html.xpath("/html/body/section/div[2]/div/article/p")
        tvDetail = tv_p_list[-1].xpath("./text()")

        aTv.setSendDateAndWeek(tvDetail[3])
        aTv.setIntState(tvDetail[11])
        aTv.story_type = tvDetail[5]
        # print(etree.tostring(tvDetail))

        # 天天美剧详细信息 每集资源
        urls = html.xpath("/html/body/section/div[2]/div/article/ol/li/a")
        baidu_cloud_urls = []
        magnet_urls = []
        ed2k_urls = []
        if urls:  # 对应在线看 和 MP4 中的栏目
            for url in urls:
                urlStr = url.attrib['href']
                if "pan.baidu.com" in urlStr:
                    baidu_cloud_urls.append(urlStr)
                elif "magnet" in urlStr:
                    magnet_urls.append(urlStr)
                elif "ed2k" in urlStr:
                    ed2k_urls.append(urlStr)
            setsNum = len(html.xpath("/html/body/section/div[2]/div/article/ol[1]/li"))


        else:  # 对应中英双语字幕中的栏目
            tableInfo = html.xpath("/html/body/section/div[2]/div/article/table[1]/tbody/tr/td[1]")
            type_len = html.xpath(
                "/html/body/section/div[2]/div/article/table[1]/tbody/tr[2]/td[1]/a")  # 取tableInfo的第一行数据
            url_type = len(type_len)
            if tableInfo:
                for t_line in tableInfo:
                    ed2k = True
                    magnet = True
                    baidu_cloud = True
                    urls = t_line.xpath("./a")
                    if len(urls) != url_type:  # 有些是总集资源，进行废弃处理 代表:http://www.meijuhui.net/archives/1907.html
                        continue
                    for url in urls:
                        urlStr = url.attrib['href']
                        if "pan.baidu.com" in urlStr and baidu_cloud:
                            baidu_cloud_urls.append(urlStr)
                            baidu_cloud = False
                        elif "magnet" in urlStr and magnet:
                            magnet_urls.append(urlStr)
                            magnet = False
                        elif "ed2k" in urlStr and ed2k:
                            ed2k_urls.append(urlStr)
                            ed2k = False
            else:
                LOGGER.info("%s 暂无资源" % aTv.tv_name)
            setsNum = max(len(baidu_cloud_urls), len(magnet_urls), len(ed2k_urls))

        for i in range(setsNum):
            tvSet = AmericanTVSets()
            tvSet.u_id = uuid.uuid1()
            tvSet.p_id = aTv.u_id
            tvSet.set_ordinal = i + 1
            if i < len(baidu_cloud_urls) - 1:
                tvSet.baidu_cloud_url = baidu_cloud_urls[i]
            if i < len(magnet_urls) - 1:
                tvSet.magnet_url = magnet_urls[i]
            if i < len(ed2k_urls) - 1:
                tvSet.ed2k_url = ed2k_urls[i]
            # print(tvSet)


if __name__ == '__main__':
    tv = AmericanTVApi("self")
    tv.scrapyTvInfo("绿箭侠第六季")
