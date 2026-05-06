# -*- coding: utf-8 -*-
"""
文章管理路由

性能优化：
- 使用分页避免大结果集
- 预加载关联数据避免 N+1
- 索引优化查询

Author: wangrui1992
Date: 2026-05-11
"""

from flask import Blueprint, render_template, request, jsonify, session, current_app
from models.article import Article
from models.tag import Tag
from models.database import db
from utils.helpers import login_required, paginate_query, success_response, error_response, log_operation
from utils.validators import Validator
from utils.cache import invalidate_cache, cache_key
from datetime import datetime

article_bp = Blueprint('article', __name__)


@article_bp.route('/list')
@login_required
def article_list():
    """文章列表页面"""
    return render_template('article/list.html')


@article_bp.route('/create')
@login_required
def create_article():
    """创建文章页面"""
    tags = Tag.query.all()
    return render_template('article/edit.html', article=None, tags=tags)


@article_bp.route('/edit/<int:article_id>')
@login_required
def edit_article(article_id):
    """编辑文章页面"""
    article = Article.query.get_or_404(article_id)
    
    # 检查权限
    if article.author_id != session['user_id'] and not session.get('is_admin'):
        return error_response('无权限编辑此文章', 'FORBIDDEN', 403)
    
    tags = Tag.query.all()
    return render_template('article/edit.html', article=article, tags=tags)


@article_bp.route('/drafts')
@login_required
def drafts():
    """草稿箱页面"""
    return render_template('article/drafts.html')


@article_bp.route('/api/list')
@login_required
def api_list():
    """
    获取文章列表 API
    
    性能优化：
    - 使用分页
    - 预加载作者信息
    - 按状态过滤
    """
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    status = request.args.get('status', 'published')
    tag_id = request.args.get('tag_id', type=int)
    keyword = request.args.get('keyword', '').strip()
    
    # 限制每页数量
    per_page = min(per_page, current_app.config.get('MAX_ITEMS_PER_PAGE', 100))
    
    # 构建查询 - 预加载作者信息避免 N+1
    query = Article.query.options(
        db.joinedload(Article.author),
        db.joinedload(Article.tags)
    )
    
    # 状态过滤
    if status == 'draft':
        query = query.filter(Article.status == 'draft')
    elif status == 'published':
        query = query.filter(Article.status == 'published')
    elif status == 'deleted':
        query = query.filter(Article.status == 'deleted')
    else:
        # 非管理员只能看到自己的
        if not session.get('is_admin'):
            query = query.filter(Article.author_id == session['user_id'])
    
    # 标签过滤
    if tag_id:
        query = query.filter(Article.tags.any(id=tag_id))
    
    # 关键词搜索（使用索引）
    if keyword:
        search = f'%{keyword}%'
        query = query.filter(
            db.or_(
                Article.title.like(search),
                Article.summary.like(search)
            )
        )
    
    # 排序
    query = query.order_by(Article.updated_at.desc())
    
    # 分页
    result = paginate_query(query, page=page, per_page=per_page)
    
    return jsonify({
        'success': True,
        'articles': [a.to_dict() for a in result['items']],
        'total': result['total'],
        'pages': result['pages'],
        'current_page': result['current_page']
    })


@article_bp.route('/api', methods=['POST'])
@login_required
def create_api():
    """创建文章 API"""
    data = request.get_json()
    
    # 验证标题
    title = data.get('title', '').strip()
    valid, msg = Validator.validate_article_title(title)
    if not valid:
        return error_response(msg, 'VALIDATION_ERROR')
    
    # 验证内容
    content = data.get('content', '')
    valid, msg = Validator.validate_article_content(content)
    if not valid:
        return error_response(msg, 'VALIDATION_ERROR')
    
    # 生成 slug
    slug = data.get('slug', '').strip()
    if not slug:
        from models.article import slugify
        slug = slugify(title)
    
    # 检查 slug 唯一性
    existing = Article.query.filter_by(slug=slug).first()
    if existing:
        slug = f'{slug}-{datetime.utcnow().strftime("%Y%m%d%H%M%S")}'
    
    # 创建文章
    article = Article(
        title=title,
        slug=slug,
        content=content,
        summary=data.get('summary', '')[:500],
        cover_image=data.get('cover_image'),
        status=data.get('status', 'draft'),
        author_id=session['user_id'],
        meta_title=data.get('meta_title'),
        meta_description=data.get('meta_description')
    )
    
    # 设置发布时间
    if article.status == 'published':
        article.publish()
    
    db.session.add(article)
    db.session.flush()  # 获取 ID
    
    # 处理标签
    tag_ids = data.get('tag_ids', [])
    if tag_ids:
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
        article.tags = tags
    
    db.session.commit()
    
    # 清除相关缓存
    invalidate_cache('article')
    
    # 记录日志
    log_operation('create', 'article', article.id, f'创建文章: {title}')
    
    return success_response(
        data={'article': article.to_dict()},
        message='文章创建成功'
    )


@article_bp.route('/api/<int:article_id>', methods=['GET'])
@login_required
def get_article(article_id):
    """获取单篇文章"""
    article = Article.query.options(
        db.joinedload(Article.author),
        db.joinedload(Article.tags)
    ).get_or_404(article_id)
    
    return success_response(data=article.to_dict(include_content=True))


@article_bp.route('/api/<int:article_id>', methods=['PUT'])
@login_required
def update_api(article_id):
    """更新文章 API"""
    article = Article.query.get_or_404(article_id)
    
    # 检查权限
    if article.author_id != session['user_id'] and not session.get('is_admin'):
        return error_response('无权限编辑此文章', 'FORBIDDEN', 403)
    
    data = request.get_json()
    
    # 更新字段
    if 'title' in data:
        article.title = data['title'].strip()
    if 'content' in data:
        article.content = data['content']
    if 'summary' in data:
        article.summary = data['summary'][:500]
    if 'slug' in data:
        article.slug = data['slug'].strip()
    if 'cover_image' in data:
        article.cover_image = data['cover_image']
    if 'status' in data:
        old_status = article.status
        article.status = data['status']
        if old_status != 'published' and data['status'] == 'published':
            article.publish()
    if 'meta_title' in data:
        article.meta_title = data['meta_title']
    if 'meta_description' in data:
        article.meta_description = data['meta_description']
    
    # 更新标签
    if 'tag_ids' in data:
        tags = Tag.query.filter(Tag.id.in_(data['tag_ids'])).all()
        article.tags = tags
    
    article.updated_at = datetime.utcnow()
    db.session.commit()
    
    # 清除缓存
    invalidate_cache('article')
    
    log_operation('update', 'article', article.id, f'更新文章: {article.title}')
    
    return success_response(
        data={'article': article.to_dict()},
        message='文章更新成功'
    )


@article_bp.route('/api/<int:article_id>', methods=['DELETE'])
@login_required
def delete_api(article_id):
    """删除文章 API（软删除）"""
    article = Article.query.get_or_404(article_id)
    
    # 检查权限
    if article.author_id != session['user_id'] and not session.get('is_admin'):
        return error_response('无权限删除此文章', 'FORBIDDEN', 403)
    
    # 软删除
    article.soft_delete()
    db.session.commit()
    
    invalidate_cache('article')
    log_operation('delete', 'article', article.id, f'删除文章: {article.title}')
    
    return success_response(message='文章已删除')


@article_bp.route('/api/<int:article_id>/publish', methods=['POST'])
@login_required
def publish_article(article_id):
    """发布文章"""
    article = Article.query.get_or_404(article_id)
    
    if article.author_id != session['user_id'] and not session.get('is_admin'):
        return error_response('无权限', 'FORBIDDEN', 403)
    
    article.publish()
    db.session.commit()
    
    invalidate_cache('article')
    log_operation('publish', 'article', article.id)
    
    return success_response(message='文章已发布')


@article_bp.route('/api/<int:article_id>/restore', methods=['POST'])
@login_required
def restore_article(article_id):
    """恢复已删除文章"""
    article = Article.query.get_or_404(article_id)
    
    if not session.get('is_admin'):
        return error_response('无权限', 'FORBIDDEN', 403)
    
    article.status = 'draft'
    article.deleted_at = None
    db.session.commit()
    
    log_operation('restore', 'article', article.id)
    
    return success_response(message='文章已恢复')
