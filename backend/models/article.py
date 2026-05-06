# -*- coding: utf-8 -*-
"""
文章模型

性能优化：
- 复合索引优化常见查询
- 反向关系使用动态查询减少内存占用
- 软删除避免物理删除导致的索引重建
- 预计算统计字段减少实时计算

Author: wangrui1992
Date: 2026-05-10
"""

from models.database import db
from datetime import datetime
import re


def slugify(text):
    """生成 URL 友好的 slug"""
    if not text:
        return ''
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:100]  # 限制长度


class Article(db.Model):
    """文章模型"""
    __tablename__ = 'articles'
    
    # 主键
    id = db.Column(db.Integer, primary_key=True)
    
    # 内容
    title = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(255), unique=True, index=True)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.String(500))
    cover_image = db.Column(db.String(255))
    
    # 状态管理
    status = db.Column(db.String(20), default='draft', index=True)  # published, draft, deleted
    
    # 预计算的统计字段（避免 COUNT 查询）
    view_count = db.Column(db.Integer, default=0, index=True)
    like_count = db.Column(db.Integer, default=0)
    comment_count = db.Column(db.Integer, default=0)
    
    # SEO
    meta_title = db.Column(db.String(255))
    meta_description = db.Column(db.String(500))
    
    # 用户和时间
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime, index=True)
    deleted_at = db.Column(db.DateTime)  # 软删除时间
    
    # 性能优化：复合索引
    __table_args__ = (
        # 常用查询组合索引
        Index('idx_article_status_published', 'status', 'published_at'),
        Index('idx_article_author_status', 'author_id', 'status'),
        Index('idx_article_status_created', 'status', 'created_at'),
        # 分页优化索引
        Index('idx_article_list_pagination', 'status', 'created_at', 'id'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )
    
    # 关系 - 标签（使用懒加载避免不必要查询）
    tags = db.relationship('Tag', secondary='article_tags', lazy='subquery',
                          backref=db.backref('articles', lazy='dynamic'))
    
    def publish(self):
        """发布文章"""
        self.status = 'published'
        self.published_at = datetime.utcnow()
    
    def to_draft(self):
        """设为草稿"""
        self.status = 'draft'
    
    def soft_delete(self):
        """软删除"""
        self.status = 'deleted'
        self.deleted_at = datetime.utcnow()
    
    def increment_views(self):
        """增加浏览量"""
        self.view_count = (self.view_count or 0) + 1
    
    def to_dict(self, include_content=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'summary': self.summary,
            'cover_image': self.cover_image,
            'status': self.status,
            'view_count': self.view_count,
            'like_count': self.like_count,
            'comment_count': self.comment_count,
            'author': self.author.to_dict() if self.author else None,
            'tags': [t.to_dict() for t in self.tags] if self.tags else [],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'published_at': self.published_at.isoformat() if self.published_at else None,
        }
        if include_content:
            data['content'] = self.content
        return data
    
    def __repr__(self):
        return f'<Article {self.title[:30]}>'


class ArticleTag(db.Model):
    """文章-标签关联表"""
    __tablename__ = 'article_tags'
    
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id', ondelete='CASCADE'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 索引优化关联查询
    __table_args__ = (
        Index('idx_article_tag_tag', 'tag_id'),
    )
