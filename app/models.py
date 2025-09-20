from peewee import PrimaryKeyField, CharField,DateTimeField,TextField
from playhouse.pool import PooledPostgresqlDatabase # 引入Postgresql连接池
from playhouse.flask_utils import FlaskDB # 引入flask-peewee
from config import DataConfig #配置
from datetime import datetime 
from peewee import fn

# 配置连接池
try:
    database = PooledPostgresqlDatabase(
        database=DataConfig.name,
        user=DataConfig.user,
        password=DataConfig.password,
        host=DataConfig.host,
        port=DataConfig.port,
        max_connections=10,  # 设置最大连接数为10
        stale_timeout=5000  # 超时的连接被自动回收
    )
except Exception as e:
    print("程序停止,数据库连接失败:", e)
    raise SystemExit(e)  # 暂停程序

# 将peewee集成到flask中
peeweeDB = FlaskDB(database=database)


# 定义模型
class Article(peeweeDB.Model):
    id = PrimaryKeyField()
    title = CharField(max_length=250) #标题
    content = TextField() #html内容
    markdown = TextField() #markdown格式
    preview = CharField() #预览
    type = CharField(max_length=20) #类型
    created_at = DateTimeField(default=datetime.now) #创建时间
    updated_at = DateTimeField(default=datetime.now) #更新时间

    #这里用于每次保存内容时，自动截取预览内容
    def save(self, *args, **kwargs):
        self.preview = fn.SUBSTR(self.markdown, 1, 220)  #存储文章预览120字
        self.updated_at = datetime.now() # 更新时间
        return super().save(*args, **kwargs)

# 获取数据库实例
DB = peeweeDB.database

