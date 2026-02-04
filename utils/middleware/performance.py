"""
性能监控中间件

记录接口耗时、SQL 查询数量、慢请求告警
"""

import time
import logging
from typing import Callable

from django.conf import settings
from django.db import connection
from django.utils.deprecation import MiddlewareMixin

from utils.logging import get_performance_logger

logger = get_performance_logger()

# 慢请求阈值（毫秒）
SLOW_REQUEST_THRESHOLD_MS = 1000

# 慢查询阈值（毫秒）
SLOW_QUERY_THRESHOLD_MS = 500


class PerformanceMiddleware(MiddlewareMixin):
    """
    性能监控中间件

    功能:
    1. 记录请求处理耗时
    2. 记录 SQL 查询数量
    3. 检测并告警慢请求
    4. 检测并记录慢查询
    """

    def __init__(self, get_response: Callable):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        # 记录开始时间
        start_time = time.perf_counter()

        # 清除查询日志（如果存在）
        queries_before = len(connection.queries) if hasattr(connection, 'queries') else 0

        # 处理请求
        response = self.get_response(request)

        # 计算耗时
        duration_ms = (time.perf_counter() - start_time) * 1000

        # 获取查询数量
        queries_after = len(connection.queries) if hasattr(connection, 'queries') else 0
        query_count = queries_after - queries_before

        # 记录性能指标
        self._log_performance(request, response, duration_ms, query_count)

        # 检测慢请求
        if duration_ms > SLOW_REQUEST_THRESHOLD_MS:
            self._log_slow_request(request, duration_ms, query_count)

        return response

    def _log_performance(
        self,
        request,
        response,
        duration_ms: float,
        query_count: int
    ) -> None:
        """记录性能指标"""
        try:
            logger.info(
                'Performance metrics',
                extra={
                    'extra_data': {
                        'path': request.path,
                        'method': request.method,
                        'status_code': response.status_code,
                        'duration_ms': round(duration_ms, 2),
                        'db_query_count': query_count,
                    }
                }
            )
        except Exception:
            pass

    def _log_slow_request(
        self,
        request,
        duration_ms: float,
        query_count: int
    ) -> None:
        """记录慢请求"""
        try:
            # 获取慢查询信息
            slow_queries = []
            if hasattr(connection, 'queries'):
                for q in connection.queries:
                    try:
                        duration = float(q.get('time', 0))
                        if duration > SLOW_QUERY_THRESHOLD_MS:
                            slow_queries.append({
                                'sql': q.get('sql', '')[:500],
                                'duration_ms': duration,
                            })
                    except (ValueError, TypeError):
                        pass

            logger.warning(
                'Slow request detected',
                extra={
                    'extra_data': {
                        'path': request.path,
                        'method': request.method,
                        'duration_ms': round(duration_ms, 2),
                        'db_query_count': query_count,
                        'threshold_ms': SLOW_REQUEST_THRESHOLD_MS,
                        'slow_queries': slow_queries[:5],  # 最多记录5个慢查询
                    }
                }
            )
        except Exception:
            pass


class SQLQueryLoggerMiddleware(MiddlewareMixin):
    """
    SQL 查询日志中间件

    记录所有 SQL 查询（仅开发环境使用）
    """

    def __init__(self, get_response: Callable):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        if not settings.DEBUG:
            return self.get_response(request)

        # 清除查询日志
        connection.queries_log.clear()

        response = self.get_response(request)

        # 记录所有查询
        for q in connection.queries:
            try:
                logger.debug(
                    f'SQL Query: {q.get("sql", "")}',
                    extra={
                        'extra_data': {
                            'sql': q.get('sql', ''),
                            'time': q.get('time', 0),
                            'params': str(q.get('params', ''))[:100],
                        }
                    }
                )
            except Exception:
                pass

        return response
