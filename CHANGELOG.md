# 更新日志

本文档记录项目的迭代开发过程。

---

## [2.0.0] - 2026-05-07

### 重大更新

项目进行全面重构，从静态博客升级为完整的 **Flask 后台管理系统**。

---

### Day 01 (2026-05-07) - 项目结构重构

- ✅ MVC 架构设计
- ✅ Flask 应用框架搭建
- ✅ 数据库模型定义（User, Article, Tag, OperationLog）
- ✅ 用户认证系统（登录/注册）
- ✅ 后台仪表盘界面
- ✅ SQL 性能优化（索引设计、查询优化）

**SQL 性能优化措施：**
- 复合索引优化登录查询
- 分页限制避免大结果集
- N+1 问题预防（joinedload）
- 软删除替代物理删除
- 预计算统计字段

---

### Day 02 (2026-05-08) - 认证系统完善

- ✅ 用户注册页面
- ✅ 密码验证增强
- ✅ 登录日志记录
- ✅ Session 管理优化
- ✅ CSRF 保护

---

### Day 03 (2026-05-09) - 表单验证与安全

- ✅ 表单验证器（Validator 类）
- ✅ XSS 防护
- ✅ SQL 注入防护
- ✅ 登录失败限制

---

### Day 04 (2026-05-10) - 文章列表管理

- ✅ 文章列表页面
- ✅ 筛选与搜索
- ✅ 分页组件
- ✅ 状态过滤（已发布/草稿/已删除）

---

### Day 05 (2026-05-11) - 文章编辑功能

- ✅ Markdown 编辑器
- ✅ 标签选择
- ✅ 摘要自动生成
- ✅ 实时保存

---

### Day 06 (2026-05-12) - 文章删除与草稿

- ✅ 软删除实现
- ✅ 草稿箱功能
- ✅ 批量操作
- ✅ 恢复已删除文章

---

### Day 07 (2026-05-13) - 标签管理系统

- ✅ 标签 CRUD
- ✅ 标签颜色
- ✅ 文章计数缓存
- ✅ 标签筛选

---

### Day 08 (2026-05-14) - 数据统计面板

- ✅ ECharts 图表集成
- ✅ 统计卡片组件
- ✅ 热门文章展示
- ✅ 用户数据概览

---

### Day 09 (2026-05-15) - 访问趋势分析

- ✅ 趋势图表
- ✅ 时间范围选择
- ✅ 数据导出
- ✅ 热门标签饼图

---

### Day 10 (2026-05-16) - 用户管理模块

- ✅ 用户列表
- ✅ 角色切换（管理员/用户）
- ✅ 账户启用/禁用
- ✅ 用户搜索

---

### Day 11 (2026-05-17) - 系统设置页面

- ✅ 基本设置
- ✅ 用户设置
- ✅ 安全设置
- ✅ 配置持久化

---

### Day 12 (2026-05-18) - 数据备份导出

- ✅ JSON 导出
- ✅ CSV 导出
- ✅ 数据导入
- ✅ 自动备份计划

---

### Day 13 (2026-05-19) - API 文档

- ✅ RESTful API 设计
- ✅ 健康检查接口
- ✅ 搜索 API
- ✅ 批量操作 API

---

### Day 14 (2026-05-20) - 性能优化

- ✅ 内存缓存系统
- ✅ 查询结果缓存
- ✅ 索引优化
- ✅ 懒加载优化

**缓存策略：**
- 热门标签缓存 5 分钟
- 统计数据缓存
- 文章列表缓存
- 手动缓存失效

---

### Day 15 (2026-05-21) - 部署与文档

- ✅ README 完善
- ✅ 部署文档
- ✅ 环境变量配置
- ✅ Docker 支持（可选）

---

## 目录结构

```
backend/
├── app.py                    # 应用入口
├── config.py                 # 配置文件
├── run.py                    # 启动脚本
├── requirements.txt          # Python 依赖
│
├── models/                   # 数据模型
│   ├── database.py          # 数据库配置与优化
│   ├── user.py              # 用户模型
│   ├── article.py           # 文章模型
│   ├── tag.py               # 标签模型
│   ├── log.py               # 日志模型
│   └── __init__.py
│
├── routes/                   # 路由
│   ├── auth.py              # 认证路由
│   ├── article.py           # 文章路由
│   ├── admin.py             # 管理路由
│   ├── api.py               # API路由
│   └── __init__.py
│
├── utils/                    # 工具函数
│   ├── helpers.py           # 辅助函数
│   ├── validators.py        # 表单验证
│   ├── cache.py             # 缓存工具
│   ├── security.py          # 安全工具
│   └── __init__.py
│
├── templates/                # HTML 模板
│   ├── auth/               # 认证页面
│   │   ├── login.html
│   │   └── register.html
│   ├── article/            # 文章页面
│   │   ├── list.html
│   │   └── edit.html
│   ├── admin/              # 管理页面
│   │   ├── users.html
│   │   ├── tags.html
│   │   ├── settings.html
│   │   └── backup.html
│   ├── dashboard.html      # 仪表盘
│   └── 404.html            # 错误页面
│
└── static/                  # 静态资源
    ├── css/
    └── js/
```

---

## SQL 性能优化总结

### 1. 索引策略
```sql
-- 登录查询优化
CREATE INDEX idx_user_login ON users(username, is_active);

-- 文章列表分页
CREATE INDEX idx_article_list_pagination ON articles(status, created_at, id);

-- 操作日志
CREATE INDEX idx_log_user_time ON operation_logs(user_id, created_at);
```

### 2. 查询优化
- 使用 `joinedload` 预加载关联数据
- 分页限制 `LIMIT` + `OFFSET`
- 避免 `SELECT *`，只查询需要的字段
- 使用数据库聚合函数代替 Python 循环

### 3. 缓存策略
- 热门数据内存缓存
- 缓存失效机制
- 按业务场景设置过期时间

### 4. 软删除
- 使用 `status` 字段标记删除
- 保留数据便于恢复
- 避免物理删除导致的索引重建
