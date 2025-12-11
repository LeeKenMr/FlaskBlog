"""
API蓝图模块
定义所有API接口，路由前缀为 /api
"""
from flask import Blueprint, request, jsonify
import env
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from sqlalchemy.exc import IntegrityError  # SQLAlchemy 错误处理
from .models import db, Article
from .common.sitemap import sitemap

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/login', methods=['POST'])
def login():
    """
    用户登录接口

    Returns:
        json: 包含 token 的响应或错误信息
    """
    # 取得请求的数据
    data = request.get_json()

    # 验证用户名和密码
    if data.get('name') != env.ADMIN_USERNAME or data.get('password') != env.ADMIN_PASSWORD:
        return jsonify({'msg': '用户名或密码错误'}), 400

    # 创建一个15天的token
    access_token = create_access_token(identity=data.get('name'), expires_delta=timedelta(days=15))
    return jsonify({'token': access_token}), 200


@api.route('/add', methods=['POST'])
@jwt_required()
def add():
    """
    添加文章接口

    Returns:
        json: 包含新文章ID的响应或错误信息
    """
    # 取得请求的数据
    data = request.get_json()

    # 写入数据库
    try:
        new_article = Article(
            title=data.get('title'),
            content=data.get('content'),
            markdown=data.get('markdown'),
            type=data.get('type')
        )
        new_article.save()  # 使用自定义的 save 方法
        return jsonify({'msg': new_article.id}), 200
    except IntegrityError as e:
        db.session.rollback()  # 回滚事务
        return jsonify({'msg': f'写入失败:{e}'}), 500


@api.route('/getwz', methods=['GET'])
@jwt_required()
def getwz():
    """
    获取文章详情接口（用于编辑）

    Returns:
        json: 包含文章 markdown 和 type 的响应
    """
    # 取得请求的数据
    article_id = request.args.get('id')

    # 读取数据库
    article = db.session.get(Article, article_id)

    if article is None:
        return jsonify({'msg': '文章不存在'}), 404

    # 返回数据
    return jsonify({'markdown': article.markdown, 'type': article.type}), 200


@api.route('/edit', methods=['POST'])
@jwt_required()
def edit():
    """
    编辑文章接口

    Returns:
        json: 更新结果响应
    """
    # 取得请求的数据
    data = request.get_json()

    # 更新数据库
    try:
        article = db.session.get(Article, data.get('id'))
        if article is None:
            return jsonify({'msg': '文章不存在'}), 404

        # 更新字段
        article.title = data.get('title')
        article.content = data.get('content')
        article.markdown = data.get('markdown')
        article.type = data.get('type')
        article.save()  # 使用自定义的 save 方法

        return jsonify({'msg': '成功更新1条数据'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'msg': f'写入失败:{e}'}), 500


@api.route('/del', methods=['POST'])
@jwt_required()
def delete():
    """
    删除文章接口

    Returns:
        json: 删除结果响应
    """
    # 取得请求的数据
    data = request.get_json()

    # 删除数据
    try:
        article = db.session.get(Article, data.get('id'))
        if article is None:
            return jsonify({'msg': '文章不存在'}), 404

        db.session.delete(article)
        db.session.commit()

        return jsonify({'msg': '成功删除1条数据'}), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'msg': f'删除失败:{e}'}), 500


@api.route('/sitemap', methods=['GET'])
@jwt_required()
def setsitemap():
    """
    生成站点地图接口

    Returns:
        json: 生成结果响应
    """
    sitemap()
    return jsonify({'msg': '生成成功'}), 200
