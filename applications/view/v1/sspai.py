import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'sspai' 的蓝图，URL 前缀为 '/sspai'
bp = Blueprint('sspai', __name__, url_prefix='/sspai')


@bp.get('/')
def sspai():
    filename = "sspai_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("少数派热榜")
        request = helper.get_html(
            "https://sspai.com/api/v1/article/tag/page/get?limit=100000&tag=%E7%83%AD%E9%97%A8%E6%96%87%E7%AB%A0",
            None,
            "dict")
        index = 1
        data_list = []
        for key in request["data"]:
            try:
                data_dict = {
                    "index": index,
                    "title": key["title"],
                    "url": "https://sspai.com/post/" + str(key["id"]),
                    "hot": key["like_count"]
                }
                index += 1
            except KeyError:
                continue
            data_list.append(data_dict)
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content