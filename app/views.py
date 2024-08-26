#这是一个视图蓝图模块，不需要引入app，将直接在app/__init__.py中引入
from flask import Blueprint, render_template,request
from .models import Article
# 将该模块注册为蓝图
view = Blueprint('view', __name__)


# 首页
@view.route('/',methods=['GET'])
def index():
    datas = Article.select().order_by(Article.id.desc()).limit(10)
    return render_template('index.html',datas=datas),200

# 分类查询
@view.route('/type/<string:type>/<int:page>',methods=['GET'])
def type(type,page=1):
     # 定义每页显示的文章数
    per_page = 12
    # 计算偏移量
    offset = (page - 1) * per_page
    # 查询文章列表，按照日期倒序排序，限制每页显示的数量
    datas = Article.select().where(Article.type==type).order_by(Article.id.desc()).offset(offset).limit(per_page)
    # 计算得到总条数
    total = Article.select().where(Article.type==type).count()
    # 计算总页数
    total_page = total // per_page if total % per_page == 0 else total // per_page + 1

    # 返回模板渲染后的HTML页面，文章列表、页码总页数
    return render_template('lists.html',datas=datas,page=page,total_page=total_page,type=type),200

# 搜索页
@view.route('/so',methods=['GET'])
def so():
    # 获取搜索关键字
    so = request.args.get('so', '')
     # 获取分页参数，默认第一页，每页显示12条
    page = int(request.args.get('page', 1))
     # 定义每页显示的文章数
    per_page = 12
    # 计算偏移量
    offset = (page - 1) * per_page
    # 搜索并分页
    datas = Article.select().where(Article.markdown.contains(so)).offset(offset).limit(per_page)
    # 计算得到总条数
    total = Article.select().where(Article.markdown.contains(so)).count()
    # 计算总页数
    total_page = total // per_page if total % per_page == 0 else total // per_page + 1
    # 返回模板渲染后的HTML页面，文章列表、页码总页数
    return render_template('so.html',datas=datas,page=page,total_page=total_page,so=so),200


# 博文章页
@view.route('/note/<int:id>',methods=['GET'])
def id(id):
    data = Article.get_or_none(Article.id == id)
    # 如果为空，返回404
    if data is None:
        return '没有找到数据',404
    return render_template('note.html',data=data),200

# 博文章页
@view.route('/us',methods=['GET'])
def us():
    return render_template('us.html'),200