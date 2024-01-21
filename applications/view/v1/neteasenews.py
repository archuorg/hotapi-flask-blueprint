import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'neteasenews' 的蓝图，URL 前缀为 '/neteasenews'
bp = Blueprint('neteasenews', __name__, url_prefix='/neteasenews')


@bp.get('/')
def neteasenews():
    filename = "neteasenews_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("网易新闻")
        request = helper.get_html("https://m.163.com/fe/api/hot/news/flow", None, "dict")
        data_list = []
        num = 1
        for key in request["data"]["list"]:
            data_dict = {"index": num,
                         "title": key["title"],
                         "url": key["url"],
                         "hot": ""}
            num += 1
            data_list.append(data_dict)
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content