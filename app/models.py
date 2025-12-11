"""
数据模型模块
使用 Flask-SQLAlchemy 定义数据库模型
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# 创建 SQLAlchemy 实例
db = SQLAlchemy()


class Article(db.Model):
    """
    文章模型

    Attributes:
        id: 主键ID
        title: 文章标题
        content: HTML内容
        markdown: Markdown格式内容
        preview: 预览内容（自动截取）
        type: 文章类型
        created_at: 创建时间
        updated_at: 更新时间
    """
    __tablename__ = 'article'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), nullable=False)  # 标题
    content = db.Column(db.Text, nullable=False)  # HTML内容
    markdown = db.Column(db.Text, nullable=False)  # Markdown格式
    preview = db.Column(db.String(255), default='')  # 预览
    type = db.Column(db.String(20), nullable=False)  # 类型
    created_at = db.Column(db.DateTime, default=datetime.now)  # 创建时间
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)  # 更新时间

    def save(self):
        """
        保存文章，自动截取预览内容

        Returns:
            Article: 当前文章实例
        """
        # 存储文章预览220字
        self.preview = self.markdown[:220] if self.markdown else ''
        self.updated_at = datetime.now()
        db.session.add(self)
        db.session.commit()
        return self

    def __repr__(self):
        return f'<Article {self.id}: {self.title}>'
