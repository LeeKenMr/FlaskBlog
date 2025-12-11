"""
Flask应用初始化模块
包括创建app实例，注册蓝图，配置数据库
"""
from flask import Flask
from flask_jwt_extended import JWTManager
import env
from .models import db, Article

# 创建app实例
app = Flask(__name__)
app.config['SECRET_KEY'] = env.SECRET_KEY
app.config['DEBUG'] = env.DEBUG

# 配置 SQLAlchemy 数据库连接
# 使用 PostgreSQL 连接字符串
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"postgresql+psycopg://{env.DATA_USERNAME}:{env.DATA_PASSWORD}"
    f"@{env.DATA_HOST}:{env.DATA_PORT}/{env.DATA_NAME}"
)
# 连接池配置
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,  # 连接池大小
    'pool_recycle': 5000,  # 连接回收时间（秒）
    'pool_pre_ping': True,  # 连接前检查连接是否有效
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁用修改追踪

# 初始化 SQLAlchemy
db.init_app(app)

# 初始化 JWT
jwt = JWTManager(app)

# 导入并注册蓝图（在 db 初始化之后导入，避免循环导入）
from .views import view
from .api import api

app.register_blueprint(view)  # 注册视图蓝图
app.register_blueprint(api)   # 注册API蓝图

# 创建表
with app.app_context():
    db.create_all()
