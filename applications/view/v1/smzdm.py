import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'smzdm' 的蓝图，URL 前缀为 '/smzdm'
bp = Blueprint('smzdm', __name__, url_prefix='/smzdm')


@bp.get('/')
def smzdm():
    filename = "smzdm_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("什么值得买热榜")
        request = helper.get_html("https://post.smzdm.com/hot_1/", None, "html")
        articles_title = request.xpath('//*[@id="feed-main-list"]/li/div/div[2]/h5/a/text()')
        articles_url = request.xpath('//*[@id="feed-main-list"]/li/div/div[2]/h5/a/@href')
        articles_hot = request.xpath('//*[@id="feed-main-list"]/li/div/div[2]/div[2]/div[2]/a[1]/span[2]/text()')
        data_list = helper.headle_html_data_list([articles_title, articles_url, articles_hot])
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content