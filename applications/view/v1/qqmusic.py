import requests
from lxml import html

import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'qqmusic' 的蓝图，URL 前缀为 '/qqmusic'
bp = Blueprint('qqmusic', __name__, url_prefix='/qqmusic')


@bp.get('/')
def qqmusic():
    filename = "qqmusic_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("QQ音乐流行榜")
        headers = {
            "coookie": "pac_uid=0_48b32310e472c; iip=0; _qimei_uuid42=18115002e341002fa0aade50be4c82a7ff5a5edf1f; _qimei_fingerprint=18f998bcb3d471c7d5965cb12f7cd8e1; _qimei_q36=; _qimei_h38=fdedf045a0aade50be4c82a702000000b18115; pgv_pvid=4126314992; fqm_pvqid=9dbed13a-c7b2-4127-b696-8416228caa5a; fqm_sessionid=e622ecfa-01b3-4fe0-bcaa-5505a33dfe2a; pgv_info=ssid=s6087019157; ts_last=y.qq.com/n/ryqq/toplist/4; ts_uid=5999908163",
            "authority": "y.qq.com",
            "referer": "https://www.google.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        }

        url = "https://y.qq.com/n/ryqq/toplist/4"

        response = requests.get(url=url, headers=headers)
        # Assuming that 'response.text' contains the HTML content
        html_content = response.text

        # Parse the HTML content
        tree = html.fromstring(html_content)

        # Use XPath to extract the desired value
        xpath_title = '//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li/div/div[3]/span/a[2]/@title'
        xpath_url = '//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li/div/div[3]/span/a[2]/@href'
        xpath_hot = '//*[@id="app"]/div/div[2]/div[2]/div[3]/ul[2]/li/div/div[2]/text()'

        articles_title = tree.xpath(xpath_title)
        articles_url = tree.xpath(xpath_url)
        articles_hot = tree.xpath(xpath_hot)

        datas = [articles_title, articles_url, articles_hot]
        data_list = helper.headle_html_data_list(datas, "https://y.qq.com", "热度")
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content