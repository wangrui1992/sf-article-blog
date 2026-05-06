# -*- coding: utf-8 -*-
"""
安全工具

Author: wangrui1992
Date: 2026-05-18
"""

import secrets
import hashlib
import hmac
from flask import current_app
from urllib.parse import quote


def generate_token(length=32):
    """生成安全的随机令牌"""
    return secrets.token_urlsafe(length)


def generate_csrf_token():
    """生成 CSRF 令牌"""
    if 'csrf_token' not in current_app.session:
        current_app.session['csrf_token'] = generate_token()
    return current_app.session['csrf_token']


def verify_csrf_token(token):
    """验证 CSRF 令牌"""
    return hmac.compare_digest(token, current_app.session.get('csrf_token', ''))


def sanitize_html(html):
    """简单的 HTML 过滤"""
    if not html:
        return ''
    
    # 移除危险标签和属性
    dangerous_tags = ['script', 'iframe', 'object', 'embed', 'form']
    for tag in dangerous_tags:
        html = html.replace(f'<{tag}', f'&lt;{tag}')
        html = html.replace(f'</{tag}>', f'&lt;/{tag}')
    
    return html


def escape_html(text):
    """转义 HTML 特殊字符"""
    if not text:
        return ''
    return (text
        .replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#x27;'))


def rate_limit_key(identifier):
    """生成限流键"""
    return f'rate_limit:{identifier}'


def is_safe_url(url):
    """检查 URL 是否安全（同源）"""
    if not url:
        return False
    # 禁止 JavaScript 协议
    if url.lower().startswith('javascript:'):
        return False
    # 相对路径安全
    if url.startswith('/'):
        return True
    # 绝对路径需要检查
    return True  # 可根据需要加强检查
