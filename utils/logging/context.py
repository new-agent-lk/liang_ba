"""
日志系统 - 上下文管理模块

使用 ContextVar 管理请求链路追踪信息
"""

from contextvars import ContextVar
from typing import Any, Dict, Optional
import uuid

# 请求上下文存储
_request_context: ContextVar[Dict[str, Any]] = ContextVar(
    'request_context', default={}
)


def set_context(**kwargs) -> None:
    """
    设置请求上下文

    Args:
        **kwargs: 上下文键值对
    """
    _request_context.set({**_request_context.get(), **kwargs})


def get_context(key: str, default: Any = None) -> Any:
    """
    获取上下文值

    Args:
        key: 上下文键名
        default: 默认值

    Returns:
        上下文值，不存在则返回默认值
    """
    return _request_context.get().get(key, default)


def get_trace_id() -> str:
    """
    获取或生成 trace_id

    Returns:
        当前请求的 trace_id
    """
    ctx = _request_context.get()
    if 'trace_id' not in ctx:
        return str(uuid.uuid4())
    return ctx['trace_id']


def get_request_id() -> str:
    """
    获取请求 ID

    Returns:
        当前请求的 request_id
    """
    ctx = _request_context.get()
    if 'request_id' not in ctx:
        return '-'
    return ctx['request_id']


def get_user_id() -> Optional[int]:
    """
    获取用户 ID

    Returns:
        当前用户 ID，未登录返回 None
    """
    return get_context('user_id')


def get_client_ip() -> str:
    """
    获取客户端 IP

    Returns:
        客户端 IP 地址
    """
    return get_context('client_ip', '-')


def clear_context() -> None:
    """清除上下文"""
    _request_context.set({})


def get_full_context() -> Dict[str, Any]:
    """
    获取完整上下文

    Returns:
        完整上下文字典
    """
    return _request_context.get().copy()
