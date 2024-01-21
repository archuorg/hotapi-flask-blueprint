from flask import Blueprint, render_template

# 创建名为 'index' 的蓝图，URL 前缀为 '/'
bp = Blueprint('index', __name__, url_prefix='/')

# 定义首页路由
@bp.get('/')
def index():
    # 渲染名为 'index.html' 的模板，并返回渲染后的内容
    return render_template('/index.html')
