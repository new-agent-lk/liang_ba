"""
日志系统 - 过滤器模块

提供敏感信息过滤、请求上下文注入等功能
"""

import re
import logging
import time
from typing import Any, Dict, Optional


class RequestContextFilter(logging.Filter):
    """
    请求上下文过滤器

    自动从 ContextVar 获取上下文信息并注入日志记录
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._context_module = None

    def filter(self, record: logging.LogRecord) -> bool:
        """注入请求上下文信息"""
        try:
            from utils.logging.context import get_context
            record.trace_id = get_context('trace_id', '-')
            record.request_id = get_context('request_id', '-')
            record.user_id = get_context('user_id')
            record.client_ip = get_context('client_ip', '-')
        except Exception:
            # 如果获取上下文失败，使用默认值
            record.trace_id = '-'
            record.request_id = '-'
            record.user_id = None
            record.client_ip = '-'
        return True


class SensitiveDataFilter(logging.Filter):
    """
    敏感信息过滤器

    自动脱敏日志中的敏感信息（密码、token、银行卡号等）
    """

    # 敏感字段名称（正则匹配，不区分大小写）
    SENSITIVE_FIELDS = [
        'password', 'passwd', 'pwd',
        'token', 'access_token', 'refresh_token', 'api_key', 'apikey',
        'secret', 'client_secret', 'jwt_secret',
        'credit_card', 'card_number', 'cvv', 'cvv2',
        'ssn', 'social_security',
        'private_key', 'privatekey',
    ]

    # 敏感字段的正则模式
    FIELD_PATTERN = re.compile(
        rf'({"|".join(SENSITIVE_FIELDS)})["\']?\s*[:=]\s*["\']?([^"\'\s,}}]+)',
        re.IGNORECASE
    )

    # 通用敏感值模式（可能是 API key、token 等）
    VALUE_PATTERNS = [
        re.compile(r'sk-[a-zA-Z0-9]{20,}'),  # OpenAI API Key
        re.compile(r'eyJ[a-zA-Z0-9_-]*\.eyJ[a-zA-Z0-9_-]*\.[a-zA-Z0-9_-]*'),  # JWT
        re.compile(r'[A-Za-z0-9+/]{40,}'),  # Base64 编码的密钥
        re.compile(r'\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}'),  # 银行卡号
    ]

    MASK = '***REDACTED***'

    def filter(self, record: logging.LogRecord) -> bool:
        """过滤敏感信息"""
        try:
            # 过滤消息中的敏感信息
            if hasattr(record, 'msg') and isinstance(record.msg, str):
                record.msg = self._redact_sensitive_data(record.msg)

            # 过滤 extra_data 中的敏感信息
            if hasattr(record, 'extra_data') and isinstance(record.extra_data, dict):
                record.extra_data = self._redact_dict(record.extra_data)

            # 过滤参数中的敏感信息
            if hasattr(record, 'args') and record.args:
                record.args = tuple(
                    self._redact_sensitive_data(str(arg))
                    if isinstance(arg, str) else arg
                    for arg in record.args
                )
        except Exception:
            # 过滤失败不影响日志记录
            pass
        return True

    def _redact_sensitive_data(self, text: str) -> str:
        """脱敏文本中的敏感信息"""
        # 脱敏字段值
        text = self.FIELD_PATTERN.sub(
            lambda m: f'{m.group(1)}={self.MASK}',
            text
        )

        # 脱敏通用敏感值模式
        for pattern in self.VALUE_PATTERNS:
            text = pattern.sub(self.MASK, text)

        return text

    def _redact_dict(self, data: Dict) -> Dict:
        """递归脱敏字典中的敏感信息"""
        result = {}
        for key, value in data.items():
            key_lower = key.lower()
            # 检查键名是否敏感
            if any(sensitive in key_lower for sensitive in self.SENSITIVE_FIELDS):
                result[key] = self.MASK
            elif isinstance(value, dict):
                result[key] = self._redact_dict(value)
            elif isinstance(value, str):
                result[key] = self._redact_sensitive_data(value)
            else:
                result[key] = value
        return result


class RateLimitFilter(logging.Filter):
    """
    速率限制过滤器

    防止日志风暴，对相同日志进行限流
    """

    def __init__(
        self,
        rate: int = 100,
        per: int = 60,
        cache_size: int = 1000,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.rate = rate  # 允许的最大日志数
        self.per = per   # 时间窗口（秒）
        self.cache_size = cache_size  # 缓存大小
        self._cache: Dict[str, tuple] = {}  # (count, first_time)
        self._cache_order: list = []  # 缓存顺序，用于清理旧条目

    def filter(self, record: logging.LogRecord) -> bool:
        """检查速率限制"""
        # 生成缓存 key
        key = self._get_key(record)

        now = time.time()

        # 清理过期条目
        self._cleanup(now)

        # 检查是否超出限制
        if key in self._cache:
            count, first_time = self._cache[key]
            elapsed = now - first_time

            if elapsed < self.per:
                # 在时间窗口内
                if count >= self.rate:
                    return False  # 超出限制，丢弃
                self._cache[key] = (count + 1, first_time)
            else:
                # 时间窗口已过，重置
                self._cache[key] = (1, now)
                self._cache_order.append(key)
        else:
            # 新条目
            self._cache[key] = (1, now)
            self._cache_order.append(key)

        # 限制缓存大小
        while len(self._cache) > self.cache_size:
            old_key = self._cache_order.pop(0)
            self._cache.pop(old_key, None)

        return True

    def _get_key(self, record: logging.LogRecord) -> str:
        """生成缓存 key"""
        # 使用日志器名称 + 级别 + 消息前缀作为 key
        return f'{record.name}:{record.levelno}:{record.getMessage()[:100]}'

    def _cleanup(self, now: float) -> None:
        """清理过期的缓存条目"""
        expired = [
            key for key, (_, first_time) in self._cache.items()
            if now - first_time > self.per
        ]
        for key in expired:
            self._cache.pop(key, None)
            if key in self._cache_order:
                self._cache_order.remove(key)
