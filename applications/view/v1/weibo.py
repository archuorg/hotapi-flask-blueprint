import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'weibo' 的蓝图，URL 前缀为 '/weibo'
bp = Blueprint('weibo', __name__, url_prefix='/weibo')


@bp.get('/')
def weibo():
    filename = "weibo_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("微博热榜")
        request = helper.get_html("https://weibo.com/ajax/statuses/hot_band", "https://weibo.com/", "dict")
        data_list = []

        for key in request["data"]["band_list"]:
            try:
                data_dict = {"index": key["realpos"],
                             "title": key["word"],
                             "url": "https://s.weibo.com/weibo?q=%23" + key["word"] + "%23",
                             "hot": str(round(key["raw_hot"] / 10000, 1)) + "万"
                             }
                data_list.append(data_dict)
            except KeyError:
                continue
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content