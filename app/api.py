#一个蓝图模块，定义api，这里的所有路由前面都会加上/api
from flask import Blueprint,request,jsonify
from config import AdminConfig # 引入配置
from flask_jwt_extended import create_access_token,jwt_required # 引入jwt
from datetime import timedelta
from peewee import IntegrityError # 打印数据库错误
from .models import Article
from .common.sitemap import sitemap

api = Blueprint('api', __name__,url_prefix='/api')



#定义一个post方法,接收josn，并返回接收到的json
@api.route('/login',methods=['POST'])
def login():
    #取得请求的数据
    data = request.get_json()
    # 这里是判断验证码的其他逻辑
    
    if data.get('name') != AdminConfig.username or data.get('password') != AdminConfig.password:
        return jsonify({'msg': '用户名或密码错误'}), 400

    # 创建一个15天的token
    access_token = create_access_token(identity=data.get('name'),expires_delta=timedelta(days=15))
    return jsonify({'token': access_token}),200


#定义一个post方法,接收josn，并返回接收到的json
#jwt只允许登录用户访问

@api.route('/add',methods=['POST'])
@jwt_required()
def add():
    #取得请求的数据
    data = request.get_json()
    #写入数据库
    try:
        new_article = Article.create(
            title=data.get('title'),
            content=data.get('content'),
            markdown=data.get('markdown'),
            type=data.get('type')
        )
        # 如果写入成功，打印新记录的 ID
        return jsonify({'msg': new_article.id}),200
    except IntegrityError as e:
        return jsonify({'msg': f'写入失败:{e}'}),500
    
@api.route('/getwz',methods=['GET'])
@jwt_required()
def getwz():
    #取得请求的数据
    article_id = request.args.get('id')
    #读取数据库
    article = Article.get(id=article_id)
    #返回数据
    return jsonify({'markdown': article.markdown,'type':article.type}),200

@api.route('/edit',methods=['POST'])
@jwt_required()
def edit():
    #取得请求的数据
    data = request.get_json()
    #写入数据库
    try:
        save_article = Article.update(
            title=data.get('title'),
            content=data.get('content'),
            markdown=data.get('markdown'),
            type=data.get('type')).where(Article.id == data.get('id')).execute()
        # 如果写入成功，打印新记录的 ID
        return jsonify({'msg': f'成功更新{save_article}条数据'}),200
    except IntegrityError as e:
        return jsonify({'msg': f'写入失败:{e}'}),500


@api.route('/del',methods=['POST'])
@jwt_required()
def delete():
    #取得请求的数据
    data = request.get_json()
    #写入数据库
    try:
        del_article = Article.delete().where(Article.id == data.get('id')).execute()
        # 如果写入成功，打印新记录的 ID
        return jsonify({'msg': f'成功删除{del_article}条数据'}),200
    except IntegrityError as e:
        return jsonify({'msg': f'删除失败:{e}'}),500
    

@api.route('/sitemap',methods=['GET'])
@jwt_required()
def setsitemap():
    sitemap()
    return jsonify({'msg': '生成成功'}),200


    