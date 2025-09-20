#这里是初始化设置，包括创建app实例，注册蓝图，配置app，配置peewee
from flask import Flask
from flask_jwt_extended import JWTManager
import env
from .views import view
from .api import api
from .models import peeweeDB, DB, Article

# 创建app实例
app = Flask(__name__)
app.config['SECRET_KEY'] = env.SECRET_KEY
app.config['DEBUG'] = env.DEBUG


jwt = JWTManager(app) # 初始化jwt
app.register_blueprint(view) #注册视图蓝图
app.register_blueprint(api) #注册api蓝图

# 将peewee集成到flask中
peeweeDB.init_app(app)


# 创建表
with app.app_context():
    DB.create_tables([Article])

