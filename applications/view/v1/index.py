from flask import Blueprint, render_template

# 创建名为 'index' 的蓝图，URL 前缀为 '/'
bp = Blueprint('index', __name__, url_prefix='/')

# 访问计数文件路径
visit_count_file = 'static/visit_count.txt'

def get_visit_count():
    try:
        with open(visit_count_file, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        # 如果文件不存在，则返回默认值0
        return 0

def set_visit_count(count):
    with open(visit_count_file, 'w') as file:
        file.write(str(count))

# 初始访问计数
visit_count = get_visit_count()

# 定义首页路由
@bp.get('/')
def index():
    global visit_count
    visit_count += 1

    # 将新的访问计数写入文件
    set_visit_count(visit_count)

    # 渲染名为 'index.html' 的模板，并返回渲染后的内容
    return render_template('/index.html', visit_count=visit_count)

