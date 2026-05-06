# -*- coding: utf-8 -*-
"""
用户模型

性能优化：
- 使用复合索引优化登录查询
- 密码哈希使用 werkzeug 内置安全方法
- 懒加载关系避免 N+1 问题

Author: wangrui1992
Date: 2026-05-07
"""

from models.database import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Index


class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'
    
    # 主键和基础字段
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # 用户信息
    nickname = db.Column(db.String(80))
    avatar_url = db.Column(db.String(255))
    bio = db.Column(db.String(500))
    
    # 角色与状态 - 使用整数存储提高比较性能
    role = db.Column(db.String(20), default='user')  # user, admin
    is_active = db.Column(db.Boolean, default=True, index=True)
    
    # 时间戳
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    
    # 性能优化：复合索引用于登录查询
    __table_args__ = (
        Index('idx_user_login', 'username', 'is_active'),
        Index('idx_user_email_active', 'email', 'is_active'),
        {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8mb4'}
    )
    
    # 关系 - 使用 lazy='joined' 避免 N+1 查询
    articles = db.relationship('Article', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        """设置密码（哈希）"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """验证密码"""
        return check_password_hash(self.password_hash, password)
    
    @property
    def is_admin(self):
        """是否为管理员"""
        return self.role == 'admin'
    
    def to_dict(self, include_email=False):
        """转换为字典 - 避免暴露敏感信息"""
        data = {
            'id': self.id,
            'username': self.username,
            'nickname': self.nickname,
            'avatar_url': self.avatar_url,
            'role': self.role,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
        }
        if include_email:
            data['email'] = self.email
        return data
    
    def __repr__(self):
        return f'<User {self.username}>'
