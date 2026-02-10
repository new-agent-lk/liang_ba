"""
日志系统 - 公共 API

提供便捷的日志器获取方法和公共接口
"""

import logging
from typing import Optional

# 默认日志器名称
DEFAULT_LOGGER = "app"


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    获取日志器

    Args:
        name: 日志器名称，如果为 None 则返回默认日志器

    Returns:
        日志器实例
    """
    logger_name = name or DEFAULT_LOGGER
    return logging.getLogger(logger_name)


# 便捷方法
def get_request_logger() -> logging.Logger:
    """获取请求日志器"""
    return logging.getLogger("app.request")


def get_error_logger() -> logging.Logger:
    """获取错误日志器"""
    return logging.getLogger("app.error")


def get_performance_logger() -> logging.Logger:
    """获取性能日志器"""
    return logging.getLogger("app.performance")


def get_security_logger() -> logging.Logger:
    """获取安全审计日志器"""
    return logging.getLogger("app.security")


def get_django_logger() -> logging.Logger:
    """获取 Django 框架日志器"""
    return logging.getLogger("django")


def get_django_request_logger() -> logging.Logger:
    """获取 Django 请求日志器"""
    return logging.getLogger("django.request")
