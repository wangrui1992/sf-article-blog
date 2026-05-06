# SegmentFault 博客后台管理系统

基于 SegmentFault 文章数据的 Flask 后台管理系统，支持文章管理、用户管理、标签管理、数据可视化等完整功能。

## 功能特性

### 核心功能
- **文章管理**：创建、编辑、发布、删除文章，支持 Markdown 编辑器和标签管理
- **用户管理**：用户注册登录、角色权限管理（作者/管理员）、状态启用/禁用
- **标签系统**：灵活的标签 CRUD 操作，支持自定义颜色和别名
- **草稿箱**：自动保存文章草稿，防止内容丢失
- **软删除机制**：数据安全删除，支持恢复

### 数据可视化
- **仪表盘统计**：总文章数、总用户数、总标签数、本月新增
- **趋势图表**：ECharts 折线图展示文章发布趋势
- **热门标签**：饼图展示标签分布
- **最新文章**：实时展示最近发布的文章列表

### 系统管理
- **系统设置**：基本配置、用户设置、安全设置
- **数据备份**：JSON/CSV 格式导出导入
- **操作日志**：完整记录用户操作行为
- **健康检查**：系统运行状态监控

## 技术栈

### 后端
- **框架**：Flask 2.3+ (应用工厂模式)
- **ORM**：SQLAlchemy 2.0 (软删除、复合索引)
- **认证**：Flask-Login + Flask-WTF (CSRF 保护)
- **缓存**：内存缓存系统 (SimpleCache + @cached 装饰器)

### 前端
- **模板引擎**：Jinja2
- **图表库**：ECharts 5.x
- **样式**：原生 CSS (GitHub Dark 风格)

### 数据库
- **类型**：SQLite (开发环境) / PostgreSQL (生产环境)
- **性能优化**：复合索引、joinedload 预加载、内存缓存

## 目录结构

```
sf-article-blog/
├── README.md                 # 项目说明文档
├── LICENSE                   # MIT 开源协议
├── CHANGELOG.md              # 更新日志
├── requirements.txt          # Python 依赖
├── index.html                # 静态首页
├── fetch_articles.py         # 文章抓取脚本
├── sample_data.json          # 示例数据
│
└── backend/
    ├── app.py                # Flask 应用入口 (create_app)
    ├── config.py             # 配置文件
    ├── run.py                # 启动脚本
    ├── requirements.txt      # Python 依赖
    │
    ├── models/               # 数据模型层
    │   ├── database.py       # 数据库初始化 & 分页工具
    │   ├── user.py           # 用户模型
    │   ├── article.py         # 文章模型
    │   ├── tag.py             # 标签模型
    │   ├── log.py             # 操作日志模型
    │   └── __init__.py
    │
    ├── routes/               # 路由控制器层
    │   ├── auth.py           # 认证路由 (登录/注册/登出)
    │   ├── article.py        # 文章路由 (CRUD/API)
    │   ├── admin.py          # 管理后台路由
    │   ├── api.py            # API 接口路由
    │   └── __init__.py
    │
    ├── utils/                # 工具函数层
    │   ├── helpers.py        # 通用辅助函数
    │   ├── validators.py     # 表单验证器
    │   ├── cache.py          # 缓存装饰器
    │   ├── security.py        # 安全工具
    │   └── __init__.py
    │
    └── templates/           # Jinja2 模板
        ├── dashboard.html     # 仪表盘
        ├── 404.html           # 错误页面
        ├── auth/
        │   ├── login.html     # 登录页
        │   └── register.html  # 注册页
        ├── article/
        │   ├── list.html      # 文章列表
        │   └── edit.html      # 文章编辑器
        └── admin/
            ├── users.html     # 用户管理
            ├── tags.html      # 标签管理
            ├── settings.html  # 系统设置
            └── backup.html    # 数据备份
```

## 快速开始

### 环境要求
- Python 3.8+
- pip 包管理器

### 安装步骤

1. **克隆项目**
```bash
git clone <repository-url>
cd sf-article-blog
```

2. **创建虚拟环境**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **安装依赖**
```bash
pip install -r requirements.txt
```

4. **初始化数据库**
```bash
cd backend
python run.py
```

5. **访问系统**
打开浏览器访问：`http://localhost:5000`

默认管理员账号：
- 用户名：`admin`
- 密码：`admin123`

## API 接口

### 认证接口
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/auth/login` | 用户登录 |
| POST | `/auth/register` | 用户注册 |
| GET | `/auth/logout` | 用户登出 |
| GET | `/api/profile` | 获取当前用户信息 |
| POST | `/api/profile` | 更新用户资料 |
| POST | `/api/change-password` | 修改密码 |

### 文章接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/article/list` | 文章列表 (分页/筛选) |
| POST | `/article/create` | 创建文章 |
| POST | `/article/update/<id>` | 更新文章 |
| POST | `/article/delete/<id>` | 删除文章 |
| POST | `/article/publish/<id>` | 发布文章 |
| GET | `/article/drafts` | 草稿箱 |

### 管理接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/admin/users` | 用户列表 |
| POST | `/admin/users/role` | 修改用户角色 |
| POST | `/admin/users/status` | 启用/禁用用户 |
| GET | `/admin/tags` | 标签列表 |
| POST | `/admin/tags/create` | 创建标签 |
| PUT | `/admin/tags/<id>` | 更新标签 |
| DELETE | `/admin/tags/<id>` | 删除标签 |
| GET | `/admin/backup` | 备份管理页面 |
| POST | `/admin/backup/export` | 导出数据 |
| POST | `/admin/backup/import` | 导入数据 |

### 数据接口
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/stats` | 仪表盘统计数据 |
| GET | `/api/trend` | 趋势数据 |
| GET | `/api/search` | 搜索接口 |
| GET | `/api/export/csv` | 导出 CSV |
| GET | `/api/health` | 健康检查 |
| POST | `/api/batch` | 批量操作 |

## SQL 性能优化

| 优化项 | 实现方式 |
|--------|----------|
| 复合索引 | `idx_user_login(username, is_active)` 加速登录查询 |
| 分页限制 | `LIMIT` + `OFFSET`，`per_page` 最大 100 条 |
| N+1 预防 | `db.joinedload(Article.author)` 预加载作者信息 |
| 软删除 | `status` 字段标记，`deleted_at` 时间戳保留数据 |
| 聚合优化 | `db.func.count()` / `db.func.sum()` 聚合查询 |
| 缓存策略 | 热门标签 5 分钟内存缓存 |
| 索引覆盖 | 只查询索引字段，避免回表查询 |

## 15 天迭代开发日志

详见 [CHANGELOG.md](./CHANGELOG.md)

### Day 1-3：项目初始化
- Flask 应用工厂模式搭建
- 数据库模型设计与实现
- 用户认证系统基础

### Day 4-6：核心功能
- 文章 CRUD 完整实现
- Markdown 编辑器集成
- 标签管理系统

### Day 7-9：权限与安全
- RBAC 权限控制
- CSRF 防护机制
- 表单验证强化

### Day 10-12：性能优化
- SQL 查询优化
- 内存缓存系统
- 分页组件优化

### Day 13-15：可视化与运维
- ECharts 图表集成
- 数据备份导出
- 操作日志系统

## 开发指南

### 添加新路由
```python
# backend/routes/new_module.py
from flask import Blueprint

new_bp = Blueprint('new', __name__)

@new_bp.route('/page')
def page():
    return render_template('new/page.html')
```

```python
# backend/app.py
from routes.new_module import new_bp
app.register_blueprint(new_bp, url_prefix='/new')
```

### 添加新模型
```python
# backend/models/new_model.py
from database import db

class NewModel(db.Model):
    __tablename__ = 'new_models'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
```

### 使用缓存
```python
from utils.cache import cached, invalidate_cache

@cached(timeout=300, key_prefix='data')
def get_data():
    # 耗时操作
    return result

# 清除缓存
invalidate_cache('data:get_data')
```

## 许可证

本项目基于 [MIT License](./LICENSE) 开源。

## 致谢

- [SegmentFault](https://segmentfault.com/) - 提供文章数据源
- [Flask](https://flask.palletsprojects.com/) - Web 框架
- [ECharts](https://echarts.apache.org/) - 数据可视化库
