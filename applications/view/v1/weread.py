import requests
from lxml import html

import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'weread' 的蓝图，URL 前缀为 '/weread'
bp = Blueprint('weread', __name__, url_prefix='/weread')


@bp.get('/')
def weread():
    filename = "weread_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("微信读书新书榜")
        headers = {
            "coookie": "RK=BC385GGMQh; ptcz=7249e858b2d651caf38107f9d7e6be821c1f76f809750a01764fa23a9a937ac5; pgv_pvid=2504128307; pac_uid=0_6ac9907bfcf99; iip=0; _qimei_uuid42=17c010d033b100ac8b8b4d68b80a8d873c5e11d195; _qimei_fingerprint=de8628dd176ec8931ddc053563733ef6; _qimei_q36=; _qimei_h38=21599bd58b8b4d68b80a8d870200000b417c01; _clck=3884666349|1|fii|0; fqm_pvqid=ee9349fa-1957-4752-9a33-da6fc46561a9; wr_localvid=; wr_name=; wr_avatar=; wr_gender=; wr_gid=229948474; wr_fp=3501789256",
            "authority": "weread.qq.com",
            "referer": "https://weread.qq.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

        url = "https://weread.qq.com/web/category/newbook"

        response = requests.get(url=url, headers=headers)

        # Assuming that 'response.text' contains the HTML content
        html_content = response.text

        # print(html_content)

        # Parse the HTML content
        tree = html.fromstring(html_content)

        # Use XPath to extract the desired value
        xpath_title = '//*[@id="routerView"]/div[2]/div[2]/ul/li/div[1]/div[2]/p[1]/text()'
        xpath_url = '//*[@id="routerView"]/div[2]/div[2]/ul/li/a/@href'
        xpath_hot = '//*[@id="routerView"]/div[2]/div[2]/ul/li/div[1]/div[2]/p[3]/span[3]/span/text()'

        articles_title = tree.xpath(xpath_title)
        articles_url = tree.xpath(xpath_url)
        articles_hot = tree.xpath(xpath_hot)

        datas = [articles_title, articles_url, articles_hot]
        data_list = helper.headle_html_data_list(datas, "https://weread.qq.com", "推荐值")
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content