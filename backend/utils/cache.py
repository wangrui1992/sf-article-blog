# -*- coding: utf-8 -*-
"""
缓存工具

性能优化：减少数据库查询次数

Author: wangrui1992
Date: 2026-05-20
"""

from functools import wraps
from flask import current_app
import hashlib
import json


class SimpleCache:
    """简单内存缓存"""
    
    def __init__(self):
        self._cache = {}
    
    def get(self, key):
        """获取缓存"""
        return self._cache.get(key)
    
    def set(self, key, value, timeout=None):
        """设置缓存"""
        self._cache[key] = value
    
    def delete(self, key):
        """删除缓存"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self):
        """清空缓存"""
        self._cache.clear()
    
    def has(self, key):
        """检查缓存是否存在"""
        return key in self._cache


# 全局缓存实例
cache = SimpleCache()


def cached(timeout=300, key_prefix='view'):
    """
    缓存装饰器
    
    Args:
        timeout: 缓存过期时间（秒）
        key_prefix: 缓存键前缀
    
    Usage:
        @cached(timeout=60, key_prefix='user_list')
        def get_users():
            ...
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 生成缓存键
            cache_key = f'{key_prefix}:{f.__name__}'
            if args:
                cache_key += f':{hashlib.md5(str(args).encode()).hexdigest()}'
            if kwargs:
                cache_key += f':{hashlib.md5(str(sorted(kwargs.items())).encode()).hexdigest()}'
            
            # 尝试获取缓存
            result = cache.get(cache_key)
            if result is not None:
                return result
            
            # 执行函数并缓存结果
            result = f(*args, **kwargs)
            cache.set(cache_key, result, timeout)
            
            return result
        return decorated_function
    return decorator


def invalidate_cache(key_prefix=None):
    """
    使缓存失效
    
    Usage:
        invalidate_cache('user')  # 删除所有以 user 开头的缓存
    """
    if key_prefix:
        # 删除匹配前缀的缓存
        keys_to_delete = [k for k in cache._cache.keys() if k.startswith(key_prefix)]
        for key in keys_to_delete:
            cache.delete(key)
    else:
        cache.clear()


def cache_key(*args, **kwargs):
    """生成缓存键"""
    key = ':'.join(str(arg) for arg in args)
    if kwargs:
        key += ':' + ':'.join(f'{k}={v}' for k, v in sorted(kwargs.items()))
    return key
