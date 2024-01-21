import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'thepaper' 的蓝图，URL 前缀为 '/thepaper'
bp = Blueprint('thepaper', __name__, url_prefix='/thepaper')


@bp.get('/')
def thepaper():
    filename = "thepaper_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("澎湃新闻")
        request = helper.get_html("https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar", None, "dict")
        data_list = []
        num = 1
        for key in request["data"]["hotNews"]:
            data_dict = {"index": num,
                         "title": key["name"],
                         "url": "https://www.thepaper.cn/newsDetail_forward_" + key["contId"],
                         "hot": key["praiseTimes"]}
            num += 1
            data_list.append(data_dict)
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content