#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SegmentFault 文章抓取脚本

用于从 SegmentFault 抓取指定用户的技术文章数据。

Usage:
    python fetch_articles.py

Output:
    segmentfault_<username>_articles.json - 抓取的文章数据
"""

import urllib.request
import json
import time
import sys
import os
from datetime import datetime

# 配置
USERNAME = "rui0908"
OUTPUT_FILE = f"segmentfault_{USERNAME}_articles.json"
API_URL = f"https://segmentfault.com/gateway/home/user/{USERNAME}/articles"


def fetch_page(page=1, size=20):
    """
    从 SegmentFault API 获取单页文章数据
    
    Args:
        page: 页码
        size: 每页数量
    
    Returns:
        dict: API 返回的 JSON 数据，失败返回 None
    """
    url = f"{API_URL}?page={page}&size={size}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json",
        "Referer": f"https://segmentfault.com/u/{USERNAME}/articles",
    }
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception as e:
        print(f"[ERROR] 获取第 {page} 页失败: {e}", file=sys.stderr)
        return None


def try_alternative_endpoints(page=1):
    """
    尝试多个备用 API 端点
    
    Args:
        page: 页码
    
    Returns:
        dict: 成功的 API 返回数据，全部失败返回 None
    """
    endpoints = [
        f"https://segmentfault.com/gateway/home/user/{USERNAME}/articles?page={page}&size=20",
        f"https://segmentfault.com/api/v2/user/{USERNAME}/articles?page={page}&limit=20",
        f"https://segmentfault.com/api/user/articles?userId={USERNAME}&page={page}",
        f"https://segmentfault.com/gateway/home/user/articles?page={page}&size=20&userId={USERNAME}",
    ]
    
    for url in endpoints:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Referer": f"https://segmentfault.com/u/{USERNAME}/articles",
        }
        req = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = resp.read().decode("utf-8")
                print(f"[INFO] 成功: {url}")
                print(f"[INFO] 状态码: {resp.status}")
                return json.loads(data)
        except Exception as e:
            print(f"[WARN] 端点失败: {url}")
            continue
    
    return None


def fetch_articles():
    """
    主抓取函数
    
    Returns:
        list: 文章列表
    """
    print(f"[INFO] 开始抓取用户 {USERNAME} 的文章...")
    
    # 尝试主要端点
    result = fetch_page(page=1)
    
    if not result:
        print("[INFO] 主端点失败，尝试备用端点...")
        result = try_alternative_endpoints(page=1)
    
    if not result:
        print("[ERROR] 所有 API 端点均失败")
        return None
    
    # 解析文章数据
    articles = []
    if "data" in result:
        articles = result["data"].get("items", [])
    elif "result" in result:
        articles = result["result"].get("articles", [])
    
    print(f"[INFO] 成功获取 {len(articles)} 篇文章")
    return articles


def save_to_json(articles):
    """
    将文章数据保存为 JSON 文件
    
    Args:
        articles: 文章列表
    
    Returns:
        str: 保存的文件路径
    """
    data = {
        "source": f"https://segmentfault.com/u/{USERNAME}/articles",
        "author": {
            "username": USERNAME,
            "fetch_date": datetime.now().isoformat()
        },
        "articles": articles,
        "total_count": len(articles)
    }
    
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print(f"[INFO] 数据已保存至: {OUTPUT_FILE}")
    return OUTPUT_FILE


def main():
    """主入口"""
    print("=" * 50)
    print(f"SegmentFault 文章抓取工具")
    print(f"目标用户: {USERNAME}")
    print("=" * 50)
    
    articles = fetch_articles()
    
    if articles:
        save_to_json(articles)
        print("\n[SUCCESS] 抓取完成!")
    else:
        print("\n[ERROR] 抓取失败，请检查网络或 API 是否可用")
        sys.exit(1)


if __name__ == "__main__":
    main()
