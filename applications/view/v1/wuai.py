import applications.common.utils.helper as helper

from flask import Blueprint

# 创建名为 'wuai' 的蓝图，URL 前缀为 '/wuai'
bp = Blueprint('wuai', __name__, url_prefix='/wuai')


@bp.get('/')
def wuai():
    filename = "wuai_data_*.data"
    file_content = helper.get_file_data(filename)
    if file_content is None:
        json_data = helper.init_json_data("吾爱热榜")
        # headers 信息
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "User-Agent": helper.random_user_agent(),
            'Connection': 'close'
        }

        request = helper.get_html("https://www.52pojie.cn/forum.php?mod=guide&view=hot", headers, "html", proxy_ip=None) # 这里没有使用代理ip ：proxy_ip=None
        if request == 1:
            return file_content
        articles_title = request.xpath('/html/body/div[6]/div[2]/div/div/div[3]/div[2]/table/tbody/tr/th/a[1]/text()')
        articles_url = request.xpath('/html/body/div[6]/div[2]/div/div/div[3]/div[2]/table/tbody/tr/th/a[1]/@href')
        articles_hot = request.xpath('/html/body/div[6]/div[2]/div/div/div[3]/div[2]/table/tbody/tr/th/span[1]/text()')
        datas = [articles_title, articles_url, articles_hot]
        data_list = helper.headle_html_data_list(datas, "https://www.52pojie.cn/", -2)
        return helper.end_json_data(json_data, data_list, filename)
    else:
        return file_content