#配置文件
class Config(object):
    DEBUG = True #是否调试模式
    SECRET_KEY = '' #密钥


#数据库配置
class DataConfig(object):
    name = '' #数据库名
    user = '' #用户名
    password = '' #密码
    host = 'localhost' #主机
    port = 5432 #端口

#管理员配置
class AdminConfig(object):
    username = '' #用户名
    password = '' #密码

   
