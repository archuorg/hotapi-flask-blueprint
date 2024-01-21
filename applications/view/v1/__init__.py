# 从Flask中导入必要的模块
from flask import Flask, Blueprint

# 从应用视图中导入蓝图
from applications.view.v1.index import bp as index_bp
# 导入另一个蓝图
from applications.view.v1.zhihu import bp as zhihu_bp
# from applications.view.v1.weibo import bp as weibo_bp
# from applications.view.v1.baidu import bp as baidu_bp
# from applications.view.v1.tieba import bp as tieba_bp
# from applications.view.v1.csdn import bp as csdn_bp
# from applications.view.v1.hupu import bp as hupu_bp
# from applications.view.v1.smzdm import bp as smzdm_bp
# from applications.view.v1.history import bp as history_bp
# from applications.view.v1.36krzonghe import bp as 36krzonghe_bp
# from applications.view.v1.36krrenqi import bp as 36krrenqi_bp
# from applications.view.v1.36krshoucang import bp as 36krshoucang_bp
# from applications.view.v1.sspai import bp as sspai_bp
# from applications.view.v1.douyin import bp as douyin_bp
# from applications.view.v1.bilibilihot import bp as bilibilihot_bp
# from applications.view.v1.bilibiliday import bp as bilibiliday_bp
# from applications.view.v1.acfun import bp as acfun_bp
from applications.view.v1.ghbk import bp as ghbk_bp
# from applications.view.v1.wuai import bp as wuai_bp
# from applications.view.v1.douban import bp as douban_bp
# from applications.view.v1.txnews import bp as txnews_bp
# from applications.view.v1.juejin import bp as juejin_bp



# 创建一个名为'v1_bp'的新蓝图，其URL前缀为'/v1'
v1_bp = Blueprint('v1', __name__, url_prefix='/v1')

# 定义一个函数来注册系统蓝图
def register_system_bps(app: Flask):
    # 在'v1_bp'下注册'**_bp'蓝图
    v1_bp.register_blueprint(zhihu_bp)
    # v1_bp.register_blueprint(weibo_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)
    # v1_bp.register_blueprint(ghbk_bp)

    # 使用Flask应用注册'v1_bp'蓝图
    app.register_blueprint(v1_bp)

    # 使用Flask应用注册'index_bp'蓝图
    app.register_blueprint(index_bp)