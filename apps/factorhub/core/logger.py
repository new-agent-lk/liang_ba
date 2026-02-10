"""
日志模块

使用统一的日志系统
"""

import logging

# 获取 FactorHub 日志器
logger = logging.getLogger("app.factorhub")

# 向后兼容：保留原有的 Logger 类名引用
# 新代码可以直接使用 utils.logging 中的日志器
__all__ = ["logger"]
