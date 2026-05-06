# -*- coding: utf-8 -*-
"""
工具函数

包含装饰器、分页、格式化等辅助函数

Author: wangrui1992
Date: 2026-05-10
"""

from functools import wraps
from flask import request, jsonify, session, redirect, url_for, current_app
from datetime import datetime
import hashlib
import random
import string


def login_required(f):
    """登录验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': '请先登录', 'code': 'UNAUTHORIZED'}), 401
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """管理员权限验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            if request.is_json:
                return jsonify({'error': '请先登录', 'code': 'UNAUTHORIZED'}), 401
            return redirect(url_for('auth.login'))
        if not session.get('is_admin'):
            if request.is_json:
                return jsonify({'error': '权限不足', 'code': 'FORBIDDEN'}), 403
            return jsonify({'error': '权限不足'}), 403
        return f(*args, **kwargs)
    return decorated_function


def api_login_required(f):
    """API 登录验证装饰器（返回 JSON）"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({'error': '请先登录', 'code': 'UNAUTHORIZED'}), 401
        return f(*args, **kwargs)
    return decorated_function


def generate_random_string(length=32):
    """生成随机字符串"""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def md5_hash(text):
    """MD5 哈希"""
    return hashlib.md5(text.encode()).hexdigest()


def format_datetime(dt, format='%Y-%m-%d %H:%M'):
    """格式化日期时间"""
    if not dt:
        return ''
    if isinstance(dt, str):
        return dt
    return dt.strftime(format)


def format_date(dt):
    """格式化日期"""
    return format_datetime(dt, '%Y-%m-%d')


def time_ago(dt):
    """返回相对时间"""
    if not dt:
        return ''
    now = datetime.utcnow()
    diff = now - dt
    
    if diff.days > 365:
        return f'{diff.days // 365}年前'
    elif diff.days > 30:
        return f'{diff.days // 30}月前'
    elif diff.days > 0:
        return f'{diff.days}天前'
    elif diff.seconds > 3600:
        return f'{diff.seconds // 3600}小时前'
    elif diff.seconds > 60:
        return f'{diff.seconds // 60}分钟前'
    else:
        return '刚刚'


def paginate_query(query, page=1, per_page=20, max_per_page=100):
    """
    分页辅助函数
    
    性能优化：使用应用层分页避免加载全部数据
    """
    # 参数校验
    page = max(1, page)
    per_page = min(max(1, per_page), max_per_page)
    
    # 执行分页查询
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return {
        'items': pagination.items,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
        'next_page': page + 1 if pagination.has_next else None,
        'prev_page': page - 1 if pagination.has_prev else None
    }


def get_client_ip():
    """获取客户端 IP（支持代理）"""
    if request.headers.get('X-Forwarded-For'):
        # 代理模式：取第一个 IP
        return request.headers.get('X-Forwarded-For').split(',')[0].strip()
    return request.remote_addr or ''


def get_user_agent():
    """获取 User-Agent"""
    return request.headers.get('User-Agent', '')[:500]


def log_operation(operation, resource_type=None, resource_id=None, details=None):
    """记录操作日志"""
    from models.log import OperationLog
    from models.database import db
    
    try:
        log = OperationLog(
            operation=operation,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            user_id=session.get('user_id'),
            ip_address=get_client_ip(),
            user_agent=get_user_agent()
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        # 日志记录失败不影响主流程
        print(f'[WARN] 操作日志记录失败: {e}')
        db.session.rollback()


def success_response(data=None, message='操作成功', **kwargs):
    """成功响应格式"""
    response = {'success': True, 'message': message}
    if data is not None:
        response['data'] = data
    response.update(kwargs)
    return jsonify(response)


def error_response(message, code='ERROR', status_code=400, **kwargs):
    """错误响应格式"""
    response = {'success': False, 'error': message, 'code': code}
    response.update(kwargs)
    return jsonify(response), status_code
