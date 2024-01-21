import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'index' 的蓝图，URL 前缀为 '/'
bp = Blueprint('zhihu', __name__, url_prefix='/zhihu')

# 知乎
@bp.get('/')
def zhihu():
    filename = "zhihu_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("知乎热榜")

        headers = {
            'Referer': 'https://www.zhihu.com/',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': helper.random_user_agent()
        }
        request = helper.get_html("https://www.zhihu.com/billboard", headers, "html")
        all_content = request.xpath('//*[@id="js-initialData"]/text()')
        all_content = helper.json.loads("".join(all_content))["initialState"]["topstory"]["hotList"]
        data_list = []
        num = 1
        for key in all_content:
            hot = key["target"]["metricsArea"]["text"]
            hot = str(hot).replace(" 万热度", "W").replace("热度累计中", "1w")
            data_list.append(
                {"index": num, "title": key["target"]["titleArea"]["text"], "url": key["target"]["link"]["url"],
                 "hot": hot})
            num += 1
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content