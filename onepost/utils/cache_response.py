import logging

from django.core.cache import caches
from functools import wraps
from rest_framework.response import Response


# 设置日志
logger = logging.getLogger(__name__)

# 自定义缓存装饰器
def cache_response(timeout, cache_name='default', unique_identifier=None):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            cache = caches[cache_name]
            cache_key = f"{request.path}:{request.query_params}"
            if unique_identifier:
                cache_key += f":{unique_identifier}"
            print("cache_key:", cache_key)
            # 检查缓存
            cached_data = cache.get(cache_key)
            print("cached_data:", cached_data)
            if cached_data:
                return Response(cached_data)

            # 获取新数据并缓存
            response = view_func(self, request, *args, **kwargs)
            cache.set(cache_key, response.data, timeout=timeout)
            return response
        return _wrapped_view
    return decorator


def get_cache_queryset_func(request, params, cache_name='default', unique_identifier=None):
    cache = caches[cache_name]
    cache_key = f"{request.path}:{params}:{unique_identifier}"
    # 检查缓存
    try:
        cached_data = cache.get(cache_key)
    except Exception as e:
        logger.error(f"Redis error: {e}")
        cached_data = None
    if cached_data:
        return cached_data
    return None


def set_cache_queryset_func(request, params, queryset, timeout, cache_name='default', unique_identifier=None):
    cache = caches[cache_name]
    cache_key = f"{request.path}:{params}:{unique_identifier}"
    try:
        cache.set(cache_key, queryset, timeout=timeout)
    except Exception as e:
        logger.error(f"Redis error: {e}")
    return queryset


def delete_cache_queryset_func(request, params, cache_name='default', unique_identifier=None):
    cache = caches[cache_name]
    cache_key = f"{request.path}:{params}:{unique_identifier}"
    try:
        cache.delete(cache_key)
    except Exception as e:
        logger.error(f"Redis error: {e}")
    return None


def get_cache_value_func( cache_name='default', unique_identifier=None):
    cache = caches[cache_name]
    cache_key = f"{unique_identifier}"
    try:
        cached_data = cache.get(cache_key)
    except Exception as e:
        logger.error(f"Redis error: {e}")
        cached_data = None
    print("value-get---cache_key:", cache_key)
    if cached_data:
        return cached_data
    return None


def set_cache_value_func(queryset, timeout, cache_name='default', unique_identifier=None):
    cache = caches[cache_name]
    cache_key = f"{unique_identifier}"
    print("value set---cache_key:", cache_key)
    try:
        cache.set(cache_key, queryset, timeout=timeout)
    except Exception as e:
        logger.error(f"Redis error: {e}")
    return queryset


def delete_cache_value_func(cache_name='default', unique_identifier=None):
    cache = caches[cache_name]
    cache_key = f"{unique_identifier}"
    print("value delete---cache_key:", cache_key)
    try:
        cache.delete(cache_key)
    except Exception as e:
        logger.error(f"Redis error: {e}")
    return None
