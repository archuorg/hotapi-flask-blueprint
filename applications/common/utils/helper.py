import glob
import re
import time
import requests
import datetime
import json
from lxml import etree
import random
import os
import urllib3



# 如果static目录没有data文件夹则创建一个
if not os.path.exists('static/data'):
    os.makedirs('static/data')

# 全局变量，设置更新时长（小时）
global_timeout_file = 1
# 代理地址，此设置不再生效
proxy_address = ""

# 以utf-8编码读取文件
def read_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        return content

# 删除文件
def del_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)

# 以utf-8编码写入文件
def write_file(file_path, content, input_type="w"):
    with open(file_path, input_type, encoding='utf-8') as f:
        f.write(content)

# 随机UA
def random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.72",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 Edg/84.0.522.40",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    ]
    return random.choice(user_agents)

# 获取代理IP
def get_proxy_ip():
    url = "http://api.89ip.cn/tqdl.html?api=1&num=1&port=443&address=&isp="
    response = get_html(url, None, "obj")
    reg = r'([0-9.:]+)<br>'
    return re.compile(reg).search(response.text).group(1)

# 请求数据
def get_html(url, headers, res_data_type, proxy_ip=None):
    """
    url：字符串类型，表示要访问的网址。
    headers：字典类型，包含HTTP请求头信息，用于模拟浏览器发送请求。
    res_data_type：字符串类型，指示响应数据类型，只能是html、dict
    """
    # 如果headers是字符串类型，则使用该字符串作为HTTP请求头referer的值
    if isinstance(headers, str):
        headers = {
            'referer': headers,
            'User-Agent': random_user_agent()}
    # 如果headers为None，则headers中只有UA信息
    elif headers is None:
        headers = {'User-Agent': random_user_agent()}

    # 数据请求
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    if proxy_ip is None:
        response = requests.get(url, headers=headers, verify=False)
    else:
        write_file('static/nohup.out', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "获取到的代理ip： " + proxy_ip, "a")
        proxy = {
            'https': proxy_ip
        }
        response = requests.get(url, headers=headers, verify=False, proxies=proxy)

    # 根据请求数据类型做数据处理
    if res_data_type == "html":
        return etree.HTML(response.text)
    elif res_data_type == "dict":
        return json.loads(response.text)
    elif res_data_type == "obj":
        return response

# 获取文件中的数据，如果是过期数据则删除返回None，或者找不到文件，直接返回None
def get_file_data(filename):
    # 获取文件名称
    filename_re = filename.replace("*", "(.*?)")
    file_names = glob.glob('static/data/' + filename)
    file_names_len = len(file_names)
    # 存在一个文件
    if file_names_len == 1:
        # 获取文件名及路径
        file_name = file_names[0]
        # 获取文件名中的unix 时间戳
        old_timestamp = int(re.findall(filename_re, file_name)[0])
        # 将unix时间戳转换为datetime对象
        old_timestamp_datetime_obj = datetime.datetime.fromtimestamp(int(old_timestamp))
        # 当前时间减去文件名中的unix时间戳，获取时间差
        time_diff = datetime.datetime.now() - old_timestamp_datetime_obj
        # 如果时间差大于1个小时，就删除当前查询到的文件，并返回None
        # 否则，返回文件中的数据
        # print(time_diff)
        # print(datetime.timedelta(hours=1))
        if time_diff > datetime.timedelta(hours=global_timeout_file):
            del_file(file_name)
            return None
        else:
            return read_file(file_name)
    # 不存在文件，返回None
    else:
        # 多个文件，全部删除
        if file_names_len > 1:
            [del_file(file_name) for file_name in file_names]
        return None

# json数据初始化
def init_json_data(title):
    if title == "err":
        return {"secure": False, "title": "ERROR", "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
    return {"secure": True, "title": title, "update_time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

# data_list 赋值
def headle_html_data_list(datas, url_prefix="", hot_prefix=None):
    num = 1
    data_list = []
    for title, url, hot in zip(datas[0], datas[1], datas[2]):
        data_dict = {"index": num, "title": title, "url": url_prefix + url}
        num += 1
        # 热度值均高于1W的情况，简化输出
        if hot_prefix == 10000:
            hot = "{}{}".format(round(int(hot.strip()) / 10000, 1), "万")
        # 需要删除前后字符的情况
        elif isinstance(hot_prefix, int):
            hot = hot[:hot_prefix]
        # 需要去除前后空白内容的情况
        elif hot_prefix == "bili":
            hot = hot.split()[0]
        # 需要删除指定字符的情况
        elif isinstance(hot_prefix, str):
            hot = hot.replace(hot_prefix, "")
        data_dict["hot"] = hot
        data_list.append(data_dict)
    return data_list

# json数据最后处理
def end_json_data(json_data, data_list, filename):
    json_data["data"] = data_list
    data = json.dumps(json_data, ensure_ascii=False)
    if len(data_list) > 0:
        filename_prefix = filename.split("*")[0]
        filename = filename_prefix + str(int(time.time())) + ".data"
        write_file("static/data/" + filename, data)
    return data

# 历史上的今天
def get_history_data(filename, curr_month, curr_day):
    filename_re = filename.replace("*", "(.*?)")
    file_names = glob.glob(
        'static/data/' + filename)
    file_names_len = len(file_names)
    if file_names_len == 1:
        # 获取文件名及路径
        file_name = file_names[0]
        # 获取文件名中的unix 时间戳
        old_timestamp = int(re.findall(filename_re, file_name)[0])
        # 将unix时间戳转换为datetime对象
        old_timestamp_datetime_obj = datetime.datetime.fromtimestamp(int(old_timestamp))
        if curr_month == old_timestamp_datetime_obj.month and curr_day == old_timestamp_datetime_obj.day:
            return read_file(file_name)
        else:
            del_file(file_name)
    return None