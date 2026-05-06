# -*- coding: utf-8 -*-
"""
Flask 应用配置

Author: wangrui1992
Date: 2026-05-07
"""

import os
from datetime import timedelta


class Config:
    """基础配置"""
    # 密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # 数据库
    # 使用 SQLite 便于演示，生产环境使用 PostgreSQL/MySQL
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'blog.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False  # 生产环境设为 False
    
    # 性能优化配置
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,          # 连接前检测
        'pool_recycle': 300,             # 5分钟回收连接
        'pool_size': 10,                # 连接池大小
        'max_overflow': 20,             # 最大溢出
    }
    
    # Session 配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # 生产环境设为 True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # 缓存配置
    CACHE_TYPE = 'simple'  # 生产环境使用 Redis
    CACHE_DEFAULT_TIMEOUT = 300
    
    # 分页配置
    ITEMS_PER_PAGE = 20
    MAX_ITEMS_PER_PAGE = 100
    
    # 上传配置
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'svg'}
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')


class DevelopmentConfig(Config):
    """开发环境"""
    DEBUG = True
    SQLALCHEMY_ECHO = False


class ProductionConfig(Config):
    """生产环境"""
    DEBUG = False
    SQLALCHEMY_ECHO = False
    
    # 强化安全配置
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'Strict'
    
    # Redis 缓存（需要安装 redis）
    CACHE_TYPE = 'redis'
    CACHE_REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
