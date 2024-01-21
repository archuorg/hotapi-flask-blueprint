import os
from flask import Flask

from applications.config import BaseConfig
from applications.view import init_bps

def create_app():
    # 创建 Flask 应用实例，使用绝对路径作为应用的根目录
    app = Flask(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

    # 引入配置信息，将应用配置对象设置为 BaseConfig
    app.config.from_object(BaseConfig)

    # 注册蓝图，调用 init_bps 函数初始化并注册应用中的蓝图
    init_bps(app)

    # 注册命令（被注释掉的代码）
    # init_script(app)

    # 返回创建好的 Flask 应用实例
    return app
