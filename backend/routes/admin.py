# -*- coding: utf-8 -*-
"""
管理后台路由

包含用户管理、系统设置、数据备份等功能

Author: wangrui1992
Date: 2026-05-16
"""

from flask import Blueprint, render_template, request, jsonify, session, Response, current_app
from models.user import User
from models.article import Article
from models.tag import Tag
from models.log import OperationLog, LoginLog
from models.database import db
from utils.helpers import admin_required, paginate_query, success_response, error_response, log_operation
from utils.cache import invalidate_cache
from datetime import datetime, timedelta
import json
import csv
import io

admin_bp = Blueprint('admin', __name__)


# ==================== 用户管理 ====================

@admin_bp.route('/users')
@admin_required
def users():
    """用户管理页面"""
    return render_template('admin/users.html')


@admin_bp.route('/api/users')
@admin_required
def get_users():
    """获取用户列表 API"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    keyword = request.args.get('keyword', '').strip()
    role = request.args.get('role', '')
    
    query = User.query
    
    # 关键词搜索
    if keyword:
        search = f'%{keyword}%'
        query = query.filter(
            db.or_(
                User.username.like(search),
                User.email.like(search),
                User.nickname.like(search)
            )
        )
    
    # 角色过滤
    if role:
        query = query.filter_by(role=role)
    
    query = query.order_by(User.created_at.desc())
    result = paginate_query(query, page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'users': [u.to_dict(include_email=True) for u in result['items']],
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page']
    })


@admin_bp.route('/api/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """更新用户"""
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    if 'role' in data:
        user.role = data['role']
    if 'is_active' in data:
        user.is_active = data['is_active']
    if 'nickname' in data:
        user.nickname = data['nickname']
    
    db.session.commit()
    log_operation('update_user', 'user', user.id, f'更新用户: {user.username}')
    
    return success_response(data=user.to_dict(include_email=True), message='用户更新成功')


@admin_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """删除用户（软删除）"""
    if user_id == session['user_id']:
        return error_response('不能删除自己', 'FORBIDDEN', 400)
    
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    
    log_operation('delete_user', 'user', user.id)
    
    return success_response(message='用户已删除')


# ==================== 标签管理 ====================

@admin_bp.route('/tags')
@admin_required
def tags():
    """标签管理页面"""
    return render_template('admin/tags.html')


@admin_bp.route('/api/tags', methods=['GET', 'POST'])
@admin_required
def manage_tags():
    """标签管理 API"""
    if request.method == 'GET':
        tags = Tag.query.order_by(Tag.article_count.desc()).all()
        return success_response(data=[t.to_dict() for t in tags])
    
    # POST 创建标签
    data = request.get_json()
    name = data.get('name', '').strip()
    
    from utils.validators import Validator
    valid, msg = Validator.validate_tag_name(name)
    if not valid:
        return error_response(msg, 'VALIDATION_ERROR')
    
    # 检查唯一性
    if Tag.query.filter_by(name=name).first():
        return error_response('标签已存在', 'TAG_EXISTS', 409)
    
    tag = Tag(
        name=name,
        slug=data.get('slug', name.lower()),
        color=data.get('color', '#58a6ff'),
        description=data.get('description', '')
    )
    
    db.session.add(tag)
    db.session.commit()
    
    log_operation('create_tag', 'tag', tag.id, f'创建标签: {name}')
    
    return success_response(data=tag.to_dict(), message='标签创建成功')


@admin_bp.route('/api/tags/<int:tag_id>', methods=['PUT', 'DELETE'])
@admin_required
def tag_detail(tag_id):
    """标签详情"""
    tag = Tag.query.get_or_404(tag_id)
    
    if request.method == 'DELETE':
        db.session.delete(tag)
        db.session.commit()
        return success_response(message='标签已删除')
    
    # PUT 更新
    data = request.get_json()
    if 'name' in data:
        tag.name = data['name']
    if 'color' in data:
        tag.color = data['color']
    if 'description' in data:
        tag.description = data['description']
    
    db.session.commit()
    
    return success_response(data=tag.to_dict(), message='标签更新成功')


# ==================== 系统设置 ====================

@admin_bp.route('/settings')
@admin_required
def settings():
    """系统设置页面"""
    return render_template('admin/settings.html')


@admin_bp.route('/api/settings', methods=['GET', 'PUT'])
@admin_required
def manage_settings():
    """系统设置 API"""
    # 默认设置（可扩展为数据库存储）
    default_settings = {
        'site_name': '博客管理系统',
        'site_description': '个人技术博客后台',
        'posts_per_page': 20,
        'allow_register': True,
        'maintenance_mode': False
    }
    
    if request.method == 'GET':
        return success_response(data=default_settings)
    
    # PUT 更新设置
    data = request.get_json()
    # 实际项目中应该持久化到数据库或配置文件
    # 这里仅作演示
    log_operation('update_settings', 'system', None, '更新系统设置')
    
    return success_response(message='设置已保存')


# ==================== 数据备份 ====================

@admin_bp.route('/backup')
@admin_required
def backup():
    """数据备份页面"""
    return render_template('admin/backup.html')


@admin_bp.route('/api/backup/export')
@admin_required
def export_data():
    """导出数据 API"""
    fmt = request.args.get('format', 'json')
    data_type = request.args.get('type', 'all')  # articles, users, tags, all
    
    if data_type == 'articles' or data_type == 'all':
        articles = Article.query.filter_by(status='published').all()
        articles_data = [a.to_dict(include_content=True) for a in articles]
    else:
        articles_data = []
    
    if data_type == 'users' or data_type == 'all':
        users = User.query.all()
        users_data = [u.to_dict(include_email=True) for u in users]
    else:
        users_data = []
    
    if data_type == 'tags' or data_type == 'all':
        tags = Tag.query.all()
        tags_data = [t.to_dict() for t in tags]
    else:
        tags_data = []
    
    export_data = {
        'export_time': datetime.utcnow().isoformat(),
        'articles': articles_data,
        'users': users_data,
        'tags': tags_data
    }
    
    if fmt == 'csv':
        # 生成 CSV
        output = io.StringIO()
        if articles_data:
            writer = csv.DictWriter(output, fieldnames=['id', 'title', 'summary', 'created_at', 'view_count'])
            writer.writeheader()
            for a in articles_data:
                writer.writerow({
                    'id': a['id'],
                    'title': a['title'],
                    'summary': a.get('summary', ''),
                    'created_at': a.get('created_at', ''),
                    'view_count': a.get('view_count', 0)
                })
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment;filename=blog_backup_{datetime.now().strftime("%Y%m%d")}.csv'}
        )
    
    # JSON 格式
    return success_response(data=export_data)


@admin_bp.route('/api/backup/import', methods=['POST'])
@admin_required
def import_data():
    """导入数据 API"""
    if 'file' not in request.files:
        return error_response('请选择文件', 'NO_FILE')
    
    file = request.files['file']
    if not file.filename.endswith('.json'):
        return error_response('仅支持 JSON 格式', 'INVALID_FORMAT')
    
    try:
        data = json.load(file)
        
        imported_count = 0
        if 'articles' in data:
            for a_data in data['articles']:
                if not Article.query.filter_by(slug=a_data.get('slug')).first():
                    article = Article(
                        title=a_data['title'],
                        slug=a_data.get('slug'),
                        content=a_data.get('content', ''),
                        summary=a_data.get('summary', ''),
                        status='published',
                        author_id=session['user_id']
                    )
                    db.session.add(article)
                    imported_count += 1
        
        db.session.commit()
        log_operation('import_data', 'system', None, f'导入 {imported_count} 篇文章')
        
        return success_response(message=f'成功导入 {imported_count} 条数据')
    except Exception as e:
        return error_response(f'导入失败: {str(e)}', 'IMPORT_ERROR')


# ==================== 操作日志 ====================

@admin_bp.route('/logs')
@admin_required
def logs():
    """操作日志页面"""
    return render_template('admin/logs.html')


@admin_bp.route('/api/logs')
@admin_required
def get_logs():
    """获取操作日志"""
    page = request.args.get('page', 1, type=int)
    operation = request.args.get('operation', '')
    
    query = OperationLog.query
    
    if operation:
        query = query.filter_by(operation=operation)
    
    query = query.order_by(OperationLog.created_at.desc())
    result = paginate_query(query, page=page, per_page=50)
    
    return jsonify({
        'success': True,
        'logs': [l.to_dict() for l in result['items']],
        'total': result['total'],
        'pages': result['pages']
    })
