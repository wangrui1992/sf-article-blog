# -*- coding: utf-8 -*-
"""
认证路由

包含登录、注册、登出等认证相关路由

Author: wangrui1992
Date: 2026-05-08
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from models.user import User
from models.log import LoginLog
from models.database import db
from utils.helpers import login_required, success_response, error_response, get_client_ip, get_user_agent, log_operation
from utils.validators import Validator
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'GET':
        return render_template('auth/login.html')
    
    # POST 处理登录
    data = request.get_json() if request.is_json else request.form.to_dict()
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    # 基本验证
    if not username or not password:
        return error_response('用户名和密码不能为空', 'VALIDATION_ERROR')
    
    # 查询用户（使用复合索引优化）
    user = User.query.filter_by(username=username, is_active=True).first()
    
    # 记录登录尝试
    login_log = LoginLog(
        username=username,
        ip_address=get_client_ip(),
        user_agent=get_user_agent()
    )
    
    if not user or not user.check_password(password):
        login_log.status = 'failed'
        login_log.fail_reason = 'invalid_credentials'
        db.session.add(login_log)
        db.session.commit()
        return error_response('用户名或密码错误', 'AUTH_FAILED', 401)
    
    # 登录成功
    user.last_login = datetime.utcnow()
    login_log.user_id = user.id
    login_log.status = 'success'
    
    # 保存 session
    session.permanent = True
    session['user_id'] = user.id
    session['username'] = user.username
    session['is_admin'] = user.is_admin
    
    db.session.commit()
    
    # 记录操作日志
    log_operation('login', 'user', user.id, f'用户 {username} 登录')
    
    return success_response(
        data={'redirect': '/dashboard' if user.is_admin else '/'},
        message='登录成功'
    )


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """用户注册"""
    if request.method == 'GET':
        return render_template('auth/register.html')
    
    # POST 处理注册
    data = request.get_json() if request.is_json else request.form.to_dict()
    username = data.get('username', '').strip()
    email = data.get('email', '').strip().lower()
    password = data.get('password', '')
    password_confirm = data.get('password_confirm', '')
    
    # 验证用户名
    valid, msg = Validator.validate_username(username)
    if not valid:
        return error_response(msg, 'VALIDATION_ERROR')
    
    # 验证邮箱
    valid, msg = Validator.validate_email(email)
    if not valid:
        return error_response(msg, 'VALIDATION_ERROR')
    
    # 验证密码
    valid, msg = Validator.validate_password(password)
    if not valid:
        return error_response(msg, 'VALIDATION_ERROR')
    
    if password != password_confirm:
        return error_response('两次密码不一致', 'VALIDATION_ERROR')
    
    # 检查用户是否存在（使用索引加速）
    if User.query.filter_by(username=username).first():
        return error_response('用户名已存在', 'USER_EXISTS', 409)
    
    if User.query.filter_by(email=email).first():
        return error_response('邮箱已被注册', 'EMAIL_EXISTS', 409)
    
    # 创建用户
    user = User(
        username=username,
        email=email,
        nickname=username,
        role='user'
    )
    user.set_password(password)
    
    db.session.add(user)
    db.session.commit()
    
    # 记录操作
    log_operation('register', 'user', user.id, f'新用户注册: {username}')
    
    return success_response(
        data={'redirect': '/auth/login'},
        message='注册成功，请登录'
    )


@auth_bp.route('/logout')
def logout():
    """用户登出"""
    user_id = session.get('user_id')
    username = session.get('username')
    
    log_operation('logout', 'user', user_id, f'用户 {username} 登出')
    
    session.clear()
    return redirect(url_for('auth.login'))


@auth_bp.route('/profile')
@login_required
def profile():
    """用户资料页面"""
    return render_template('auth/profile.html')


@auth_bp.route('/api/profile', methods=['GET', 'PUT'])
@login_required
def api_profile():
    """用户资料 API"""
    user = User.query.get(session['user_id'])
    
    if request.method == 'GET':
        return success_response(data=user.to_dict(include_email=True))
    
    # PUT 更新资料
    data = request.get_json()
    
    if 'nickname' in data:
        user.nickname = data['nickname']
    if 'bio' in data:
        user.bio = data['bio']
    if 'avatar_url' in data:
        user.avatar_url = data['avatar_url']
    
    db.session.commit()
    log_operation('update_profile', 'user', user.id)
    
    return success_response(data=user.to_dict(), message='资料更新成功')


@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """修改密码"""
    data = request.get_json()
    old_password = data.get('old_password', '')
    new_password = data.get('new_password', '')
    new_password_confirm = data.get('new_password_confirm', '')
    
    user = User.query.get(session['user_id'])
    
    if not user.check_password(old_password):
        return error_response('原密码错误', 'AUTH_FAILED', 401)
    
    valid, msg = Validator.validate_password(new_password)
    if not valid:
        return error_response(msg, 'VALIDATION_ERROR')
    
    if new_password != new_password_confirm:
        return error_response('两次密码不一致', 'VALIDATION_ERROR')
    
    user.set_password(new_password)
    db.session.commit()
    
    log_operation('change_password', 'user', user.id)
    
    return success_response(message='密码修改成功')
