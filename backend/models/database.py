# -*- coding: utf-8 -*-
"""
数据库配置与优化

包含数据库连接池配置、查询优化设置

Author: wangrui1992
Date: 2026-05-07
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event
from sqlalchemy.engine import Engine

db = SQLAlchemy()


def init_db(app):
    """初始化数据库"""
    db.init_app(app)
    
    with app.app_context():
        # 确保 instance 目录存在
        os.makedirs(app.instance_path, exist_ok=True)
        
        # 创建所有表
        db.create_all()
        
        # 创建默认管理员
        create_default_admin()


@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """SQL 查询日志（仅开发环境）"""
    import time
    conn.query_start_time = time.time()


@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    """记录慢查询（超过100ms）"""
    import time
    total = time.time() - conn.query_start_time
    if total > 0.1:  # 100ms
        print(f"[SLOW QUERY] {total:.3f}s: {statement[:100]}...")


def create_default_admin():
    """创建默认管理员"""
    from models.user import User
    
    if not User.query.filter_by(role='admin').first():
        admin = User(
            username='admin',
            email='admin@example.com',
            nickname='管理员',
            role='admin'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('[INFO] 默认管理员已创建: admin / admin123')


import os
