import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'csdn' 的蓝图，URL 前缀为 '/csdn'
bp = Blueprint('csdn', __name__, url_prefix='/csdn')


@bp.get('/')
def csdn():
    filename = "csdn_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("csdn热榜")
        headers = {"user-agent": helper.random_user_agent()}
        data_list = []
        num = 1
        for i in range(0, 4):
            url = "https://blog.csdn.net/phoenix/web/blog/hot-rank?page=" + str(i) + "&pageSize=25&type="
            request = helper.get_html(url, headers, "dict")
            for key in request["data"]:
                data_dict = {"index": num,
                             "title": key["articleTitle"],
                             "url": key["articleDetailUrl"],
                             "hot": key["pcHotRankScore"]}
                num += 1
                data_list.append(data_dict)
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content