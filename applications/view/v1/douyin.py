import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'douyin' 的蓝图，URL 前缀为 '/douyin'
bp = Blueprint('douyin', __name__, url_prefix='/douyin')


@bp.get('/')
def douyin():
    filename = "douyin_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("抖音热榜")
        request = helper.get_html('https://www.douyin.com/aweme/v1/web/hot/search/list/',
                           'https://www.douyin.com/', "dict")
        data_list = []
        for key in request["data"]["word_list"]:
            data_dict = {"index": key["position"],
                         "title": key["word"],
                         "url": "https://www.douyin.com/hot/" + key["sentence_id"],
                         "hot": str(round(key["hot_value"] / 10000, 1)) + "万"}
            data_list.append(data_dict)
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content