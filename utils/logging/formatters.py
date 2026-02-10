"""
日志系统 - 格式化器模块

提供 JSON 和详细格式的日志格式化器
"""

import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict, Optional


class JSONFormatter(logging.Formatter):
    """
    结构化 JSON 日志格式化器

    输出格式示例:
    {
        "timestamp": "2026-02-04T10:30:45.123Z",
        "level": "INFO",
        "logger": "app.request",
        "message": "Request completed",
        "module": "views",
        "function": "login",
        "line": 42,
        "trace_id": "abc123-def456",
        "user_id": 1,
        "extra": {...}
    }
    """

    def __init__(
        self,
        include_trace_id: bool = True,
        include_user_id: bool = True,
        include_request_id: bool = True,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.include_trace_id = include_trace_id
        self.include_user_id = include_user_id
        self.include_request_id = include_request_id

    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录为 JSON 字符串"""
        log_data: Dict[str, Any] = {
            "timestamp": self._get_timestamp(),
            "level": self._clean_levelname(record.levelname),
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "process_id": record.process,
            "thread_id": record.thread,
        }

        # 添加 trace_id
        if self.include_trace_id and hasattr(record, "trace_id"):
            log_data["trace_id"] = record.trace_id

        # 添加 request_id
        if self.include_request_id and hasattr(record, "request_id"):
            log_data["request_id"] = record.request_id

        # 添加用户信息
        if self.include_user_id and hasattr(record, "user_id"):
            log_data["user_id"] = record.user_id

        # 添加异常信息
        if record.exc_info:
            log_data["exception"] = self._format_exception(record.exc_info)

        # 添加额外字段
        if hasattr(record, "extra_data"):
            log_data["extra"] = record.extra_data

        # 添加日志特定字段
        if hasattr(record, "request_path"):
            log_data["request_path"] = record.request_path
        if hasattr(record, "request_method"):
            log_data["request_method"] = record.request_method
        if hasattr(record, "status_code"):
            log_data["status_code"] = record.status_code
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms

        return json.dumps(log_data, ensure_ascii=False, default=str)

    def _get_timestamp(self) -> str:
        """获取 ISO 格式时间戳"""
        now = datetime.now(timezone.utc)
        return now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    def _format_exception(self, exc_info) -> Optional[Dict[str, str]]:
        """格式化异常信息"""
        if not exc_info:
            return None

        return {
            "type": exc_info[0].__name__ if exc_info[0] else "Unknown",
            "message": str(exc_info[1]) if exc_info[1] else "",
            "traceback": self.formatException(exc_info) if exc_info[1] else "",
        }

    def _clean_levelname(self, levelname: str) -> str:
        """清理 ANSI 颜色代码"""
        import re

        # 移除 ANSI 转义序列
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub("", levelname)


class DetailedFormatter(logging.Formatter):
    """
    详细格式日志格式化器（带颜色）

    输出格式示例:
    [2026-02-04 10:30:45][INFO][app.request][trace_id:abc123] Request completed
    """

    # ANSI 颜色代码
    COLORS = {
        "DEBUG": "\033[36m",  # 青色
        "INFO": "\033[32m",  # 绿色
        "WARNING": "\033[33m",  # 黄色
        "ERROR": "\033[31m",  # 红色
        "CRITICAL": "\033[35m",  # 紫色
    }
    RESET = "\033[0m"

    def __init__(self, use_colors: bool = True, fmt: str = None, *args, **kwargs):
        # 默认格式
        default_fmt = "[%(asctime)s][%(levelname)s][%(name)s][trace_id:%(trace_id)s] %(message)s"
        super().__init__(fmt=fmt or default_fmt, *args, **kwargs)
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录"""
        # 确保有 trace_id
        if not hasattr(record, "trace_id"):
            record.trace_id = "-"

        # 添加颜色
        if self.use_colors and record.levelname in self.COLORS:
            record.levelname = self.COLORS[record.levelname] + record.levelname + self.RESET

        return super().format(record)


class SimpleFormatter(logging.Formatter):
    """
    简单格式日志格式化器

    输出格式示例:
    [INFO][2026-02-04 10:30:45][views.py:42] Request completed
    """

    def __init__(self, fmt: str = None, *args, **kwargs):
        default_fmt = "[%(levelname)s][%(asctime)s][%(filename)s:%(lineno)d] %(message)s"
        super().__init__(fmt=fmt or default_fmt, *args, **kwargs)

    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录"""
        return super().format(record)
