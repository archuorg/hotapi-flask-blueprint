import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'juejin' 的蓝图，URL 前缀为 '/juejin'
bp = Blueprint('juejin', __name__, url_prefix='/juejin')


@bp.get('/')
def juejin():
    filename = "juejin_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("稀土掘金")
        request = helper.get_html("https://api.juejin.cn/content_api/v1/content/article_rank?category_id=1&type=hot", None, "dict")
        data_list = []
        num = 1
        for key in request["data"]:
            data_dict = {"index": num,
                         "title": key["content"]["title"],
                         "url": 'https://juejin.cn/post/' + key["content"]["content_id"],
                         "hot": key["content_counter"]["hot_rank"]}
            num += 1
            data_list.append(data_dict)
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content