# -*- coding: utf-8 -*-
"""
表单验证器

Author: wangrui1992
Date: 2026-05-09
"""

import re
from functools import wraps
from flask import request, jsonify


class Validator:
    """表单验证器类"""
    
    @staticmethod
    def validate_username(username):
        """验证用户名"""
        if not username:
            return False, '用户名不能为空'
        if len(username) < 3:
            return False, '用户名至少3个字符'
        if len(username) > 20:
            return False, '用户名最多20个字符'
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, '用户名只能包含字母、数字和下划线'
        return True, ''
    
    @staticmethod
    def validate_email(email):
        """验证邮箱"""
        if not email:
            return False, '邮箱不能为空'
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            return False, '邮箱格式不正确'
        return True, ''
    
    @staticmethod
    def validate_password(password):
        """验证密码"""
        if not password:
            return False, '密码不能为空'
        if len(password) < 6:
            return False, '密码至少6位'
        if len(password) > 50:
            return False, '密码最多50位'
        return True, ''
    
    @staticmethod
    def validate_article_title(title):
        """验证文章标题"""
        if not title:
            return False, '标题不能为空'
        if len(title) < 2:
            return False, '标题至少2个字符'
        if len(title) > 255:
            return False, '标题最多255个字符'
        return True, ''
    
    @staticmethod
    def validate_article_content(content):
        """验证文章内容"""
        if not content:
            return False, '内容不能为空'
        if len(content) < 10:
            return False, '内容至少10个字符'
        if len(content) > 100000:
            return False, '内容最多100000个字符'
        return True, ''
    
    @staticmethod
    def validate_tag_name(name):
        """验证标签名"""
        if not name:
            return False, '标签名不能为空'
        if len(name) < 1:
            return False, '标签名至少1个字符'
        if len(name) > 50:
            return False, '标签名最多50个字符'
        if not re.match(r'^[\w\u4e00-\u9fa5]+$', name):
            return False, '标签名只能包含文字、字母、数字和下划线'
        return True, ''


def validate_request(*fields):
    """
    请求验证装饰器
    
    Usage:
        @validate_request('username', 'password')
        def login():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            data = request.get_json() or request.form.to_dict()
            
            errors = []
            for field in fields:
                if field not in data or not data[field]:
                    errors.append(f'缺少字段: {field}')
            
            if errors:
                return jsonify({'success': False, 'errors': errors}), 400
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator
