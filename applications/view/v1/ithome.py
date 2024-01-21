import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'ithome' 的蓝图，URL 前缀为 '/ithome'
bp = Blueprint('ithome', __name__, url_prefix='/ithome')


@bp.get('/')
def ithome():
    filename = "ithome_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("IT资讯最新")
        url = "https://it.ithome.com/"
        request = helper.get_html(url, 'https://it.ithome.com/', "html")
        articles_title = request.xpath(
            '//*[@id="list"]/div[1]/ul/li/div/h2/a/text()')
        articles_url = request.xpath(
            '//*[@id="list"]/div[1]/ul/li/div/h2/a/@href')
        articles_hot = request.xpath(
            '//*[@id="list"]/div[1]/ul/li/div/div[2]/div[1]/a[1]/text()')
        datas = [articles_title, articles_url, articles_hot]
        data_list = helper.headle_html_data_list(datas, "", None)
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content