import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'bilibilihot' 的蓝图，URL 前缀为 '/bilibilihot'
bp = Blueprint('bilibilihot', __name__, url_prefix='/bilibilihot')


@bp.get('/')
def bilibilihot():
    filename = "bilibilihot_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("bilibili热搜榜")
        data_list = []
        num = 1
        for index in range(1, 6):
            request = helper.get_html(f"https://api.bilibili.com/x/web-interface/popular?ps=20&pn={index}", None, "dict")
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