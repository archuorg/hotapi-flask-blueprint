import datetime

import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'krrenqi' 的蓝图，URL 前缀为 '/krrenqi'
bp = Blueprint('krrenqi', __name__, url_prefix='/krrenqi')


@bp.get('/')
def krrenqi():
    filename = "krrenqi_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("36Kr人气榜")
        url = "https://www.36kr.com/hot-list/renqi/" + datetime.datetime.now().strftime("%Y-%m-%d") + "/1"
        request = helper.get_html(url, 'https://www.36kr.com/', "html")
        articles_title = request.xpath(
            '//*[@id="app"]/div/div[2]/div[3]/div/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/p/a/text()')
        articles_url = request.xpath(
            '//*[@id="app"]/div/div[2]/div[3]/div/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/p/a/@href')
        articles_hot = request.xpath(
            '//*[@id="app"]/div/div[2]/div[3]/div/div/div[2]/div[1]/div/div/div/div/div[2]/div[2]/div/span/span/text()')
        datas = [articles_title, articles_url, articles_hot]
        data_list = helper.headle_html_data_list(datas, "https://www.36kr.com", "热度")
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content