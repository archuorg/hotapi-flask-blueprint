import datetime
import re
from lxml import etree

import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'history' 的蓝图，URL 前缀为 '/history'
bp = Blueprint('history', __name__, url_prefix='/history')


@bp.get('/')
def history():
    filename = "history_data_*.data"
    # 获取当天 月、日
    today = datetime.date.today()
    curr_month = today.month
    curr_day = today.day
    file_content = helper.get_history_data(filename, curr_month, curr_day)
    if file_content is None:
        base_url = "https://zh.wikipedia.org/wiki/{}%E6%9C%88{}%E6%97%A5".format(curr_month, curr_day)
        json_data = helper.init_json_data("历史上的今天")
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Cache-Control': 'max-age=0',
            'Cookie': 'WMF-Last-Access=28-Nov-2023; WMF-Last-Access-Global=28-Nov-2023; GeoIP=KR:11:Seoul:37.52:126.87:v4; NetworkProbeLimit=0.001; zhwikimwuser-sessionId=01024758f6f7520b528f'
        }

        request = helper.get_html(base_url, header, "html")
        articles_title = request.xpath('//*[@id="mw-content-text"]/div[1]/h3/following-sibling::ul[1]/li')
        num = 0
        data_list = []
        articles_title_num = len(articles_title)
        for title in articles_title:
            title = etree.tostring(title, encoding='unicode')
            cleaned_text = re.sub(r'<.*?>|\n', '', title)
            data_dict = {"index": articles_title_num - num,
                         "title": cleaned_text,
                         "url": "javaScript:;"}
            data_list.insert(0, data_dict)
            num += 1
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content
    # filename = "history_data_*.data"