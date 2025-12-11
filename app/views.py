"""
视图蓝图模块
定义所有前端页面路由
"""
from flask import Blueprint, render_template, request
from .models import db, Article

# 将该模块注册为蓝图
view = Blueprint('view', __name__)


@view.route('/', methods=['GET'])
def index():
    """
    首页视图

    Returns:
        html: 渲染后的首页模板，包含最新10篇文章
    """
    datas = db.session.query(Article).order_by(Article.id.desc()).limit(10).all()
    return render_template('index.html', datas=datas), 200


@view.route('/type/<string:type>/<int:page>', methods=['GET'])
def type(type, page=1):
    """
    分类文章列表视图

    Args:
        type: 文章类型
        page: 页码，默认为1

    Returns:
        html: 渲染后的列表页模板
    """
    # 定义每页显示的文章数
    per_page = 12
    # 计算偏移量
    offset = (page - 1) * per_page

    # 查询文章列表，按照日期倒序排序，限制每页显示的数量
    datas = db.session.query(Article).filter(
        Article.type == type
    ).order_by(Article.id.desc()).offset(offset).limit(per_page).all()

    # 计算得到总条数
    total = db.session.query(Article).filter(Article.type == type).count()
    # 计算总页数
    total_page = total // per_page if total % per_page == 0 else total // per_page + 1

    # 设置标题映射
    title_map = {
        'go': 'Golang',
        'py': 'Python',
        'qd': '前端',
        'uni': 'uni-app',
        'db': '数据库',
        'ser': '运维部署',
        'ai': '人工智能',
        'chain': '区块链',
        'tools': '工具软件'
    }
    title = title_map.get(type, type)

    # 返回模板渲染后的HTML页面，文章列表、页码总页数
    return render_template('lists.html', datas=datas, page=page, total_page=total_page, type=type, title=title), 200


@view.route('/so', methods=['GET'])
def so():
    """
    搜索页视图

    Returns:
        html: 渲染后的搜索结果页模板
    """
    # 获取搜索关键字
    so = request.args.get('so', '')
    # 获取分页参数，默认第一页，每页显示12条
    page = int(request.args.get('page', 1))
    # 定义每页显示的文章数
    per_page = 12
    # 计算偏移量
    offset = (page - 1) * per_page

    # 搜索并分页（使用 LIKE 进行模糊搜索）
    datas = db.session.query(Article).filter(
        Article.markdown.contains(so)
    ).offset(offset).limit(per_page).all()

    # 计算得到总条数
    total = db.session.query(Article).filter(Article.markdown.contains(so)).count()
    # 计算总页数
    total_page = total // per_page if total % per_page == 0 else total // per_page + 1

    # 返回模板渲染后的HTML页面，文章列表、页码总页数
    return render_template('so.html', datas=datas, page=page, total_page=total_page, so=so), 200


@view.route('/note/<int:id>', methods=['GET'])
def id(id):
    """
    文章详情页视图

    Args:
        id: 文章ID

    Returns:
        html: 渲染后的文章详情页模板
    """
    data = db.session.get(Article, id)
    # 如果为空，返回404
    if data is None:
        return '没有找到数据', 404
    return render_template('note.html', data=data), 200


@view.route('/us', methods=['GET'])
def us():
    """
    关于我们页面视图

    Returns:
        html: 渲染后的关于页模板
    """
    return render_template('us.html'), 200


@view.route('/chat', methods=['GET'])
def chat():
    """
    聊天页面视图

    Returns:
        html: 渲染后的聊天页模板
    """
    return render_template('chat.html'), 200
