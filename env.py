import os
from dotenv import load_dotenv
load_dotenv()

DEBUG=bool(os.getenv("DEBUG")) #是否调试模式
SECRET_KEY=os.getenv("SECRET_KEY") #密钥

# 数据库配置
DATA_NAME=os.getenv("DATA_NAME")
DATA_USERNAME=os.getenv("DATA_USERNAME")
DATA_PASSWORD=os.getenv("DATA_PASSWORD")
DATA_HOST=os.getenv("DATA_HOST")
DATA_PORT=int(os.getenv("DATA_PORT"))

# 管理员配置
ADMIN_USERNAME=os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD=os.getenv("ADMIN_PASSWORD")

# 网站配置
WEB_URL=os.getenv("WEB_URL")
WEBNAME=os.getenv("WEB_NAME")
