#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SegmentFault 博客后台管理系统

主应用入口

性能优化：
- 蓝图按需加载
- 数据库连接池配置
- 缓存中间件

Author: wangrui1992
Date: 2026-05-07
"""

from flask import Flask, render_template, jsonify, request, session, redirect, url_for, send_from_directory
from functools import wraps
import os

from config import config


def create_app(config_name='development'):
    """应用工厂函数"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # 确保上传目录存在
    os.makedirs(app.config.get('UPLOAD_FOLDER', 'uploads'), exist_ok=True)
    os.makedirs(os.path.join(app.instance_path), exist_ok=True)
    
    # 初始化数据库
    from models.database import init_db
    init_db(app)
    
    # 注册蓝图
    from routes.auth import auth_bp
    from routes.article import article_bp
    from routes.admin import admin_bp
    from routes.api import api_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(article_bp, url_prefix='/article')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # ==================== 公共路由 ====================
    
    @app.route('/')
    def index():
        """前台首页 - 静态博客"""
        return render_template('index.html')
    
    @app.route('/blog/<slug>')
    def blog_post(slug):
        """博客文章详情页"""
        from models.article import Article
        article = Article.query.filter_by(slug=slug, status='published').first()
        if not article:
            return render_template('404.html'), 404
        return render_template('blog/post.html', article=article)
    
    @app.route('/dashboard')
    def dashboard():
        """后台仪表盘 - 需要登录"""
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return render_template('dashboard.html')
    
    # ==================== 错误处理 ====================
    
    @app.errorhandler(404)
    def not_found(e):
        if request.is_json:
            return jsonify({'error': '资源不存在', 'code': 'NOT_FOUND'}), 404
        return render_template('404.html'), 404
    
    @app.errorhandler(500)
    def server_error(e):
        if request.is_json:
            return jsonify({'error': '服务器错误', 'code': 'SERVER_ERROR'}), 500
        return render_template('500.html'), 500
    
    # ==================== 请求钩子 ====================
    
    @app.before_request
    def before_request():
        """请求前处理"""
        # 记录最后活跃时间
        pass
    
    @app.after_request
    def after_request(response):
        """响应后处理"""
        # 安全头
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        return response
    
    return app


# 应用实例（开发用）
app = create_app()
