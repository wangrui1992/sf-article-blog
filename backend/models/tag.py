# -*- coding: utf-8 -*-
"""
标签模型

性能优化：
- 标签计数缓存避免频繁 COUNT
- 唯一约束保证数据一致性

Author: wangrui1992
Date: 2026-05-13
"""

from models.database import db
from datetime import datetime
from sqlalchemy import Index


class Tag(db.Model):
    """标签模型"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(50), unique=True, index=True)
    color = db.Column(db.String(20), default='#58a6ff')
    description = db.Column(db.String(255))
    
    # 缓存的文章数量（定时更新或文章变更时更新）
    article_count = db.Column(db.Integer, default=0, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_tag_name', 'name'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'color': self.color,
            'article_count': self.article_count
        }
    
    def __repr__(self):
        return f'<Tag {self.name}>'
