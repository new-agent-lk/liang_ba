"""
DRF 异常日志处理器

补充记录 DRF 已处理/未处理的接口异常，避免仅依赖 Django 中间件。
"""

from rest_framework.views import exception_handler

from utils.logging import get_error_logger

logger = get_error_logger()


def custom_exception_handler(exc, context):
    """记录 DRF 异常并委托默认处理逻辑。"""
    response = exception_handler(exc, context)

    request = context.get("request")
    view = context.get("view")
    extra_data = {
        "path": getattr(request, "path", "-"),
        "method": getattr(request, "method", "-"),
        "view": view.__class__.__name__ if view else None,
        "exception_type": type(exc).__name__,
        "exception_message": str(exc),
        "status_code": getattr(response, "status_code", 500),
        "query_string": (
            getattr(getattr(request, "META", {}), "get", lambda *_: "")("QUERY_STRING", "") or ""
        ),
    }

    if response is None:
        logger.exception("Unhandled DRF exception", extra={"extra_data": extra_data})
        return None

    log_method = logger.error if response.status_code >= 500 else logger.warning
    log_method("Handled DRF exception", extra={"extra_data": extra_data})
    return response
