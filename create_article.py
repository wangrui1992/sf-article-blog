# -*- coding: utf-8 -*-
"""通过 Flask Shell 发布文章到数据库"""

import sys
import os

# 添加 backend 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from app import create_app
from models.article import Article
from models.tag import Tag
from models.database import db

app = create_app()

with app.app_context():
    # 检查用户 rrui0908 是否存在
    from models.user import User
    user = User.query.filter_by(username='rui0908').first()
    if not user:
        print("用户 rui0908 不存在，创建中...")
        user = User(
            username='rui0908',
            email='rui0908@example.com',
            role='user'
        )
        user.set_password('rui0908')
        db.session.add(user)
        db.session.commit()
        print(f"用户已创建，ID: {user.id}")
    else:
        print(f"用户已存在，ID: {user.id}")

    # 检查文章是否已存在
    existing = Article.query.filter_by(slug='fastapi-workflow-explained').first()
    if existing:
        print("文章已存在，跳过创建。")
        print(f"文章 ID: {existing.id}, 标题: {existing.title}")
        sys.exit(0)

    # 创建文章
    content = """<h2>一、启动流程</h2>

<h3>1. 初始化阶段</h3>
<ul>
<li>加载应用配置</li>
<li>注册路由和端点</li>
<li>初始化依赖注入系统</li>
<li>生成 OpenAPI 文档</li>
</ul>

<h3>2. 服务器启动</h3>
<ul>
<li>启动 ASGI 服务器（如 Uvicorn）</li>
<li>绑定端口，开始监听请求</li>
</ul>

<h2>二、请求处理流程</h2>

<h3>1. 请求接收</h3>
<ul>
<li>客户端发送 HTTP 请求到服务器</li>
<li>ASGI 服务器接收请求并传递给 FastAPI 应用</li>
</ul>

<h3>2. 路由匹配</h3>
<ul>
<li>FastAPI 根据请求的 HTTP 方法和路径匹配对应的端点</li>
<li>使用树状结构高效匹配路由，支持路径参数和查询参数</li>
</ul>

<h3>3. 依赖解析</h3>
<ul>
<li>解析请求中的依赖项（如路径参数、查询参数、请求体等）</li>
<li>执行依赖注入，获取所需的依赖对象</li>
<li>验证依赖项的类型和值</li>
</ul>

<h3>4. 请求验证</h3>
<ul>
<li>根据类型提示验证请求数据</li>
<li>使用 Pydantic 模型验证请求体</li>
<li>检查路径参数和查询参数的类型</li>
<li>验证失败时返回 422 Unprocessable Entity 错误</li>
</ul>

<h3>5. 端点执行</h3>
<ul>
<li>调用匹配的端点函数</li>
<li>传入解析后的参数</li>
<li>执行业务逻辑</li>
</ul>

<h3>6. 响应生成</h3>
<ul>
<li>收集端点函数的返回值</li>
<li>根据返回值类型自动转换为适当的响应格式</li>
<li>设置响应状态码和头信息</li>
<li>处理异常，生成错误响应</li>
</ul>

<h3>7. 响应发送</h3>
<ul>
<li>将响应返回给 ASGI 服务器</li>
<li>ASGI 服务器将响应发送回客户端</li>
</ul>

<h2>三、核心组件</h2>

<h3>1. 路由系统</h3>
<ul>
<li>基于 Starlette 的路由系统</li>
<li>支持路径参数、查询参数、请求体等</li>
<li>支持嵌套路由和路由器</li>
</ul>

<h3>2. 依赖注入</h3>
<ul>
<li>强大的依赖注入系统</li>
<li>支持嵌套依赖</li>
<li>可用于认证、数据库连接等场景</li>
</ul>

<h3>3. 数据验证</h3>
<ul>
<li>基于 Pydantic 模型</li>
<li>自动类型检查和验证</li>
<li>生成详细的错误信息</li>
</ul>

<h3>4. 文档生成</h3>
<ul>
<li>自动生成 OpenAPI 文档</li>
<li>支持 Swagger UI 和 ReDoc</li>
<li>基于类型提示和文档字符串</li>
</ul>

<h3>5. 中间件</h3>
<ul>
<li>支持全局和路由级中间件</li>
<li>可用于日志记录、CORS 处理等</li>
</ul>

<h2>四、执行示例</h2>

<p>以下是一个简单的 FastAPI 应用及其执行流程：</p>

<pre><code>from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
async def create_item(item: Item):
    return {"item": item}
</code></pre>

<p><strong>执行流程</strong>：</p>
<ol>
<li>应用启动，注册 <code>/items/</code> 端点</li>
<li>客户端发送 POST 请求到 <code>/items/</code>，携带 JSON 数据 <code>{"name": "Test", "price": 10.0}</code></li>
<li>FastAPI 匹配到 <code>/items/</code> 端点</li>
<li>解析请求体，使用 Pydantic 验证数据</li>
<li>执行 <code>create_item</code> 函数，传入验证后的 <code>item</code> 对象</li>
<li>函数返回 <code>{"item": item}</code></li>
<li>FastAPI 将返回值转换为 JSON 响应</li>
<li>响应发送回客户端，状态码为 200 OK</li>
</ol>

<h2>五、性能优化特点</h2>

<h3>1. 异步支持</h3>
<ul>
<li>基于 ASGI 标准</li>
<li>支持异步端点和依赖</li>
<li>高并发处理能力</li>
</ul>

<h3>2. 类型提示</h3>
<ul>
<li>利用 Python 3.6+ 的类型提示</li>
<li>提供更好的 IDE 支持</li>
<li>减少运行时错误</li>
</ul>

<h3>3. 自动文档</h3>
<ul>
<li>无需额外配置，自动生成 API 文档</li>
<li>提高开发和测试效率</li>
</ul>

<h3>4. 高效路由</h3>
<ul>
<li>基于树状结构的路由匹配</li>
<li>减少路由匹配时间</li>
</ul>

<h3>5. 内存优化</h3>
<ul>
<li>合理的内存使用</li>
<li>适合处理大量并发请求</li>
</ul>

<h2>六、总结</h2>

<p>FastAPI 的工作流程设计合理，结合了现代 Python 特性和高性能 Web 框架的优点。它通过类型提示、依赖注入和自动文档生成等特性，提供了一种简洁、高效、类型安全的 Web 开发体验。同时，基于 ASGI 的异步支持使其在处理高并发请求时表现出色，适合构建现代 API 和微服务。</p>

<p>通过了解 FastAPI 的工作流程，你可以更好地利用它的特性，构建高性能、可维护的 Web 应用。</p>"""

    article = Article(
        title='FastAPI 工作流程详解',
        slug='fastapi-workflow-explained',
        content=content,
        summary='详解 FastAPI 的完整工作流程，包括启动流程、请求处理、核心组件和性能优化特点。',
        status='published',
        author_id=user.id,
        meta_title='FastAPI 工作流程详解',
        meta_description='详解 FastAPI 的完整工作流程，包括启动流程、请求处理、核心组件和性能优化特点。',
        view_count=0,
        like_count=0,
        comment_count=0
    )

    # 发布时间
    from datetime import datetime
    article.published_at = datetime.utcnow()

    db.session.add(article)
    db.session.commit()

    print(f"文章创建成功！")
    print(f"ID: {article.id}")
    print(f"标题: {article.title}")
    print(f"Slug: {article.slug}")
    print(f"状态: {article.status}")
    print(f"访问地址: <ADDRESS_REMOVED>
