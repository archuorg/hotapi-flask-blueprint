import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'baidu' 的蓝图，URL 前缀为 '/baidu'
bp = Blueprint('baidu', __name__, url_prefix='/baidu')


@bp.get('/')
def baidu():
    filename = "baidu_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("百度热榜")
        request = helper.get_html('https://top.baidu.com/board?tab=realtime', 'https://www.baidu.com/', "html")
        articles_title = request.xpath('//*[@id="sanRoot"]/main/div[2]/div/div[2]/div/div[2]/a/div[1]/text()')
        articles_url = request.xpath('//*[@id="sanRoot"]/main/div[2]/div/div[2]/div/div[2]/a/@href')
        articles_hot = request.xpath('//*[@id="sanRoot"]/main/div[2]/div/div[2]/div/div[1]/div[2]/text()')
        datas = [articles_title, articles_url, articles_hot]
        data_list = helper.headle_html_data_list(datas, "", 10000)
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content