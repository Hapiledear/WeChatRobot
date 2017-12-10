# -*- coding: utf-8 -*-
import logging

import requests

LOGGER = logging.getLogger(__name__)

url_get_latest = 'https://movie.douban.com/j/search_subjects?type=tv&tag={0}&sort={1}&page_limit=15&page_start=0'

doubang_tag_map = {'美剧': '%E7%BE%8E%E5%89%A7', '韩剧': '%E9%9F%A9%E5%89%A7', '日剧': '%E6%97%A5%E5%89%A7',
                   '国产': '%E5%9B%BD%E4%BA%A7%E5%89%', '港剧': '%E6%B8%AF%E5%89%A7'}
session = requests.Session()
header_info = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}

session.headers.update(header_info)

def getLatestList(type):
    reqUrl = url_get_latest.format(doubang_tag_map[type],"time")
    LOGGER.debug("请求url=%s " % reqUrl)
    response = session.get(reqUrl)  # get请求方式，并设置请求头



if __name__ == '__main__':
    getLatestList('美剧')