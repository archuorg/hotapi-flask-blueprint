import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'bilibiliday' 的蓝图，URL 前缀为 '/bilibiliday'
bp = Blueprint('bilibiliday', __name__, url_prefix='/bilibiliday')


@bp.get('/')
def bilibiliday():
    filename = "bilibiliday_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("哔哩哔哩全站日榜")
        request = helper.get_html("https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all", None, "dict")
        data_list = []
        num = 1
        for key in request["data"]["list"]:
            if key["stat"]["vv"] > 10000:
                hot = "{}{}".format(round(key["stat"]["vv"] / 10000, 1), "万")
            else:
                hot = key["stat"]["vv"]
            data_list.append({"index": num, "title": key["title"],
                              "url": 'https://www.bilibili.com/video/' + key["short_link_v2"].split('/')[-1],
                              "hot": hot})
            num += 1
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content