import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'douban' 的蓝图，URL 前缀为 '/douban'
bp = Blueprint('douban', __name__, url_prefix='/douban')


@bp.get('/')
def douban():
    filename = "douban_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("豆瓣新片榜")
        request = helper.get_html('https://movie.douban.com/chart', 'https://movie.douban.com/chart', "html")
        articles_title = request.xpath('//*[@id="content"]/div/div[1]/div/div/table/tr/td[1]/a/@title')
        articles_url = request.xpath('//*[@id="content"]/div/div[1]/div/div/table/tr/td[2]/div/a/@href')
        articles_hot = request.xpath('//*[@id="content"]/div/div[1]/div/div/table/tr/td[2]/div/div/span[2]/text()')
        c1 = []
        c2 = []
        c3 = []

        for title, url, hot in zip(articles_title, articles_url, articles_hot):
            c1.append(str(title))
            c2.append(str(url))
            c3.append(str(hot))
        datas = [c1, c2, c3]
        data_list = helper.headle_html_data_list(datas, "")
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content