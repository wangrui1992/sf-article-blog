# SegmentFault 文章展示博客

一个精美的静态博客页面，展示博主在 [SegmentFault](https://segmentfault.com) 上的技术文章。

## 项目结构

```
.
├── index.html          # 个人博客主页面
├── fetch_articles.py   # 文章数据抓取脚本
├── data/               # 文章数据目录
│   └── sample_data.json
├── src/                # 源代码目录（可选扩展）
└── README.md
```

## 功能特点

- 🎨 **精美 UI** - 深色主题，现代设计
- 📱 **响应式布局** - 适配各种设备
- ⚡ **快速加载** - 纯静态页面，无需后端
- 🔗 **原文链接** - 点击跳转到 SegmentFault 阅读全文

## 技术栈

- HTML5 + CSS3 + Vanilla JavaScript
- Google Fonts (Inter + JetBrains Mono)
- 无需任何框架或构建工具

## 本地运行

直接用浏览器打开 `index.html` 即可：

```bash
# macOS
open index.html

# Windows
start index.html

# Linux
xdg-open index.html
```

或使用任意本地服务器：

```bash
# Python 3
python -m http.server 8000

# Node.js
npx serve .
```

然后访问 http://localhost:8000

## 更新文章数据

1. 运行 `fetch_articles.py` 抓取最新文章数据
2. 将生成的 JSON 文件放入 `data/` 目录
3. 更新 `index.html` 中的文章内容

## 关于博主

**瑞0908** - 专注 Python 爬虫技术、Scrapy 框架实战与后端开发。

- SegmentFault 主页：https://segmentfault.com/u/rui0908
- 写作年限：8年+
- 文章数量：91篇+

## License

MIT License
