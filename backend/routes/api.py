# -*- coding: utf-8 -*-
"""
API 接口路由

包含数据统计、图表数据等 API

性能优化：
- 使用聚合查询代替循环计算
- 缓存热点数据
- 限制返回数据量

Author: wangrui1992
Date: 2026-05-14
"""

from flask import Blueprint, request, jsonify, Response, current_app
from models.article import Article
from models.user import User
from models.tag import Tag
from models.database import db
from utils.helpers import api_login_required, login_required, success_response
from utils.cache import cache, cache_key, invalidate_cache
from datetime import datetime, timedelta
import json

api_bp = Blueprint('api', __name__)


# ==================== 统计数据 ====================

@api_bp.route('/stats/overview')
@login_required
def stats_overview():
    """
    统计概览 API
    
    性能优化：
    - 使用数据库聚合函数代替 Python 循环
    - 限制时间范围避免全表扫描
    """
    today = datetime.utcnow().date()
    week_ago = today - timedelta(days=7)
    month_ago = today - timedelta(days=30)
    
    # 使用单个查询获取基础统计
    base_stats = db.session.query(
        db.func.count(Article.id).label('total_articles'),
        db.func.sum(Article.view_count).label('total_views'),
        db.func.count(User.id).label('total_users')
    ).join(User, Article.author_id == User.id).filter(
        Article.status == 'published',
        User.is_active == True
    ).first()
    
    # 本周新增文章
    weekly_articles = Article.query.filter(
        Article.status == 'published',
        Article.published_at >= week_ago
    ).count()
    
    # 本月新增文章
    monthly_articles = Article.query.filter(
        Article.status == 'published',
        Article.published_at >= month_ago
    ).count()
    
    # 今日活跃用户（简化版：有文章更新的用户）
    active_users = db.session.query(db.func.count(db.func.distinct(Article.author_id))).filter(
        Article.updated_at >= week_ago
    ).scalar() or 0
    
    # 热门文章（浏览量最高）
    popular_articles = Article.query.filter_by(status='published')\
        .order_by(Article.view_count.desc())\
        .limit(5)\
        .all()
    
    return jsonify({
        'success': True,
        'data': {
            'total_articles': base_stats.total_articles or 0,
            'total_views': int(base_stats.total_views or 0),
            'total_users': base_stats.total_users or 0,
            'weekly_articles': weekly_articles,
            'monthly_articles': monthly_articles,
            'active_users': active_users,
            'popular_articles': [a.to_dict() for a in popular_articles]
        }
    })


@api_bp.route('/stats/trend')
@login_required
def stats_trend():
    """获取趋势数据（用于图表）"""
    days = request.args.get('days', 7, type=int)
    days = min(days, 90)  # 限制最大范围
    
    # 生成日期列表
    data = []
    for i in range(days - 1, -1, -1):
        date = datetime.utcnow().date() - timedelta(days=i)
        
        # 单日文章发布数（使用索引优化）
        article_count = Article.query.filter(
            db.func.date(Article.published_at) == date
        ).count()
        
        # 单日浏览量（简化版，实际应该记录每日浏览明细）
        view_count = 0
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'articles': article_count,
            'views': view_count
        })
    
    return jsonify({
        'success': True,
        'data': data
    })


@api_bp.route('/stats/tags')
@login_required
def stats_tags():
    """获取标签统计数据"""
    # 按文章数量排序的标签
    tags = Tag.query.order_by(Tag.article_count.desc()).limit(20).all()
    
    return jsonify({
        'success': True,
        'data': [t.to_dict() for t in tags]
    })


# ==================== 搜索 ====================

@api_bp.route('/search')
@login_required
def search():
    """全文搜索 API"""
    keyword = request.args.get('q', '').strip()
    if not keyword:
        return jsonify({'success': True, 'data': []})
    
    # 限制结果数量
    limit = min(request.args.get('limit', 20, type=int), 50)
    
    search = f'%{keyword}%'
    
    # 搜索文章
    articles = Article.query.filter(
        Article.status == 'published',
        db.or_(
            Article.title.like(search),
            Article.summary.like(search),
            Article.content.like(search)
        )
    ).limit(limit).all()
    
    return jsonify({
        'success': True,
        'data': [a.to_dict() for a in articles],
        'total': len(articles)
    })


# ==================== 导出功能 ====================

@api_bp.route('/export')
@login_required
def export():
    """导出数据"""
    fmt = request.args.get('format', 'json')
    data_type = request.args.get('type', 'articles')
    
    if data_type == 'articles':
        # 预加载关联数据避免 N+1
        articles = Article.query.options(
            db.joinedload(Article.author),
            db.joinedload(Article.tags)
        ).filter_by(status='published').all()
        
        if fmt == 'csv':
            return export_articles_csv(articles)
        
        return jsonify({
            'success': True,
            'data': [a.to_dict(include_content=True) for a in articles],
            'total': len(articles),
            'export_time': datetime.utcnow().isoformat()
        })
    
    return jsonify({'success': False, 'error': '不支持的数据类型'})


def export_articles_csv(articles):
    """导出文章为 CSV 格式"""
    import csv
    import io
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    # 写入表头
    writer.writerow(['ID', '标题', '摘要', '作者', '浏览量', '发布时间', '标签'])
    
    # 写入数据
    for a in articles:
        writer.writerow([
            a.id,
            a.title,
            a.summary or '',
            a.author.username if a.author else '',
            a.view_count or 0,
            a.published_at.strftime('%Y-%m-%d') if a.published_at else '',
            ','.join([t.name for t in a.tags])
        ])
    
    output.seek(0)
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={
            'Content-Disposition': f'attachment;filename=articles_{datetime.now().strftime("%Y%m%d")}.csv'
        }
    )


# ==================== 标签接口 ====================

@api_bp.route('/tags')
def get_tags():
    """获取标签列表（公开接口）"""
    # 缓存热门标签
    cache_key_name = 'api:tags:popular'
    cached_data = cache.get(cache_key_name)
    
    if cached_data:
        return jsonify({'success': True, 'data': cached_data})
    
    tags = Tag.query.order_by(Tag.article_count.desc()).limit(50).all()
    tags_data = [t.to_dict() for t in tags]
    
    # 缓存 5 分钟
    cache.set(cache_key_name, tags_data, 300)
    
    return jsonify({'success': True, 'data': tags_data})


# ==================== 健康检查 ====================

@api_bp.route('/health')
def health_check():
    """健康检查接口"""
    try:
        # 检查数据库连接
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.utcnow().isoformat()
        }), 500


# ==================== 批量操作 ====================

@api_bp.route('/batch/delete', methods=['POST'])
@login_required
def batch_delete():
    """批量删除文章"""
    data = request.get_json()
    article_ids = data.get('ids', [])
    
    if not article_ids:
        return jsonify({'success': False, 'error': '请选择要删除的文章'})
    
    # 限制数量
    article_ids = article_ids[:100]
    
    # 批量软删除
    Article.query.filter(Article.id.in_(article_ids)).update(
        {'status': 'deleted', 'deleted_at': datetime.utcnow()},
        synchronize_session=False
    )
    db.session.commit()
    
    invalidate_cache('article')
    
    return jsonify({
        'success': True,
        'message': f'已删除 {len(article_ids)} 篇文章'
    })


@api_bp.route('/batch/publish', methods=['POST'])
@login_required
def batch_publish():
    """批量发布文章"""
    data = request.get_json()
    article_ids = data.get('ids', [])
    
    if not article_ids:
        return jsonify({'success': False, 'error': '请选择要发布的文章'})
    
    article_ids = article_ids[:100]
    
    now = datetime.utcnow()
    Article.query.filter(Article.id.in_(article_ids)).update(
        {'status': 'published', 'published_at': now},
        synchronize_session=False
    )
    db.session.commit()
    
    invalidate_cache('article')
    
    return jsonify({
        'success': True,
        'message': f'已发布 {len(article_ids)} 篇文章'
    })
