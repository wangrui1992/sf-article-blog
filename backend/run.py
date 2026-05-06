#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SegmentFault 博客后台管理系统 - 启动入口

Author: wangrui1992
Date: 2026-05-07
"""

import os
from app import create_app

# 创建应用实例
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app()

if __name__ == '__main__':
    # 开发环境运行
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
