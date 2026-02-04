"""
异常捕获中间件

捕获并记录所有未处理异常
"""

import traceback
import logging
from typing import Callable, Optional

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings

from utils.logging import get_error_logger

logger = get_error_logger()


class ExceptionLoggingMiddleware(MiddlewareMixin):
    """
    异常捕获中间件

    功能:
    1. 捕获所有未处理异常
    2. 记录异常完整信息（类型、消息、堆栈）
    3. 包含请求上下文信息
    4. 返回 None 继续默认异常处理
    """

    def __init__(self, get_response: Callable):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        return self.get_response(request)

    def process_exception(
        self,
        request: HttpRequest,
        exception: Exception
    ) -> Optional[HttpResponse]:
        """处理异常"""
        # 获取异常信息
        exc_type = type(exception).__name__
        exc_message = str(exception)
        exc_traceback = traceback.format_exc()

        # 记录异常日志
        logger.exception(
            f'Unhandled exception: {exc_type}',
            extra={
                'extra_data': {
                    'path': request.path,
                    'method': request.method,
                    'exception_type': exc_type,
                    'exception_message': exc_message,
                    'traceback': exc_traceback,
                    'query_string': request.META.get('QUERY_STRING', '') or '',
                }
            }
        )

        # 返回 None 继续默认异常处理
        return None


class ErrorResponseMiddleware(MiddlewareMixin):
    """
    错误响应中间件

    统一处理错误响应格式
    """

    def __init__(self, get_response: Callable):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)

        # 如果是错误状态码且 DEBUG=False，记录错误响应
        if response.status_code >= 400 and not getattr(settings, 'DEBUG', False):
            logger.warning(
                'Error response',
                extra={
                    'extra_data': {
                        'path': request.path,
                        'method': request.method,
                        'status_code': response.status_code,
                    }
                }
            )

        return response
