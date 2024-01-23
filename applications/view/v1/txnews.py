import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'txnews' 的蓝图，URL 前缀为 '/txnews'
bp = Blueprint('txnews', __name__, url_prefix='/txnews')


@bp.get('/')
def txnews():
    filename = "txnews_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("腾讯新闻")
        request = helper.get_html("https://r.inews.qq.com/gw/event/hot_ranking_list?page_size=50", None,
                           "dict")
        data_list = []
        num = 1
        for key in request["idlist"]:
            for news_item in key["newslist"][1:]:
                data_dict = {"index": num,
                             "title": news_item["title"],
                             "url": news_item["surl"],
                             "hot": ""}
                num += 1
                data_list.append(data_dict)
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content