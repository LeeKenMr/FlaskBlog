# flask简易博客

- 响应式tailwindcss，前端使用SSR渲染对搜索引擎友好
- 数据库:PostgreSQL+peewee

## 使用到的环境
数据库:`sudo apt-get install postgresql-14`
需要pip安装的python包:
- flask
- Flask-JWT-Extended
- peewee
- psycopg2-binary
- gunicorn


## 试运行
编辑config.py配置文件，填写所有项
后端运行:直接运行run.py
后台管理员运行:
`cd vue`
`npm install`
`npm run dev`

## tailwindcss构建

> 构建时需要编辑tailwind.config.js，构建前台还是后台

后台构建`npx tailwindcss -i ./tailwind.css -o ./vue/public/static/admin.css`

前台构建`npx tailwindcss -i ./tailwind.css -o ./app/static/main.css`

```
项目目录
 ┣ app                  #应用目录
 ┃ ┣ templates          #模板文件
 ┃ ┃ ┣ base.html        #基础模板  
 ┃ ┃ ┗ index.html       #首页模板
 ┃ ┣ static             #静态文件
 ┃ ┣ __init__.py        #初始化app实列
 ┃ ┣ models.py          #peewee模型
 ┃ ┣ views.py           #视图路由
 ┃ ┗ api.py             #api路由
 ┣ vue                  #后台管理
 ┃ ┣ .........          #
 ┃ ┗ ......             #
 ┣ run.py               #运行文件
 ┣ config.py            #配置文件
 ┣ requirements.txt     #依赖文件
 ┗ tailwindss...		#一些tailwindcss项目文件
```

## 部署步骤
上传程序后，将所有py文件设置为运行权限
为应用下面创建一个虚拟python环境
在blog目录下创建一个jingtai文件夹
然后static目录放置在jingtai下
将后台vue构建的文件上传到jingtai文件夹

1. `python3 -m venv /home/blog/venv` 创建虚拟环境
2. `source /home/blog/venv/bin/activate` 激活
3. pip安装依赖


### 使用gunicorn启动flask
创建系统启动文件/etc/systemd/system/blog.service:
```
[Unit]
Description=blog
After=network.target

[Service]
User=root
Group=www-data
WorkingDirectory=/home/blog
ExecStart=/home/blog/venv/bin/gunicorn run:app --chdir /home/blog -w 2 -b 127.0.0.1:5000
Restart=always
Environment="PATH=/home/blog/venv/bin:/usr/local/bin:/usr/bin:/bin"

[Install]
WantedBy=multi-user.target
```
启动/home/blog目录下的run.py中的app实例对象
注意上面的的配置运行环境均指向应用下的虚拟python环境

## caddy配置
```
www.abc.cn {
	file_server
	root * /home/blog/app/jingtai/
	#ser 服务器处理路由
	@ser {
        path / /so /note/* /us /type/* /api/*
    }
	#转发给5000端口
	handle @ser {
		reverse_proxy localhost:5000
	}
	# SPA 路由处理
    @vue {
        path /admin /admin/*
    }
    rewrite @vue /admin.html
}
```

### 常用命令
`sudo systemctl daemon-reload` 刷新系统启动配置

`sudo systemctl start blog` 启动

`sudo systemctl restart blog` 重启

`sudo systemctl status blog` 查看运行

`sudo systemctl stop blog` 停止

`sudo systemctl enable blog` 开机自启动

`sudo systemctl disable blog`   禁止自启动

`sudo journalctl -u blog.service -r` 查看错误




