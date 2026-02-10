"""
请求追踪中间件

生成并注入 trace_id，记录请求生命周期
"""

import time
import uuid
from typing import Callable

from django.utils.deprecation import MiddlewareMixin

from utils.logging import get_request_logger
from utils.logging.context import set_context

logger = get_request_logger()


class RequestTraceMiddleware(MiddlewareMixin):
    """
    请求追踪中间件

    功能:
    1. 生成或获取 trace_id
    2. 设置请求上下文（trace_id, request_id, user_id, client_ip）
    3. 记录请求开始和完成
    4. 在响应头中添加 trace_id 和 request_id
    """

    def __init__(self, get_response: Callable):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request):
        # 生成或获取 trace_id
        trace_id = request.headers.get("X-Trace-ID") or str(uuid.uuid4())
        request_id = str(uuid.uuid4())[:8]

        # 获取客户端 IP
        client_ip = self._get_client_ip(request)

        # 设置上下文
        set_context(
            trace_id=trace_id,
            request_id=request_id,
            user_id=getattr(request.user, "id", None),
            client_ip=client_ip,
        )

        # 记录请求开始
        request._start_time = time.perf_counter()
        request._trace_id = trace_id
        request._request_id = request_id

        # 记录请求开始日志
        self._log_request_started(request)

        # 处理请求
        response = self.get_response(request)

        # 计算耗时
        duration_ms = (time.perf_counter() - request._start_time) * 1000

        # 记录请求完成日志
        self._log_request_completed(request, response, duration_ms)

        # 添加响应头
        response["X-Trace-ID"] = trace_id
        response["X-Request-ID"] = request_id

        return response

    def _log_request_started(self, request) -> None:
        """记录请求开始"""
        try:
            logger.info(
                "Request started",
                extra={
                    "extra_data": {
                        "method": request.method,
                        "path": request.path,
                        "query_string": request.META.get("QUERY_STRING", "") or "",
                        "user_agent": request.headers.get("User-Agent", "-")[:200],
                    }
                },
            )
        except Exception:
            pass  # 日志记录失败不应影响请求处理

    def _log_request_completed(self, request, response, duration_ms: float) -> None:
        """记录请求完成"""
        try:
            logger.info(
                "Request completed",
                extra={
                    "extra_data": {
                        "method": request.method,
                        "path": request.path,
                        "status_code": response.status_code,
                        "duration_ms": round(duration_ms, 2),
                    }
                },
            )
        except Exception:
            pass

    def _get_client_ip(self, request) -> str:
        """获取客户端真实 IP"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # 取第一个 IP（最原始的客户端）
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "-")
