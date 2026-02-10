"""
安全审计中间件

记录安全相关事件（登录、权限变更、敏感操作等）
"""

from typing import Callable, Optional

from django.http import HttpRequest, HttpResponse
from django.utils.deprecation import MiddlewareMixin

from utils.logging import get_security_logger

logger = get_security_logger()

# 需要审计的路径
AUDIT_PATHS = [
    "/admin/",
    "/api/auth/",
    "/api/users/",
    "/api/auth/login/",
    "/api/auth/logout/",
    "/api/auth/register/",
]

# 需要审计的方法
AUDIT_METHODS = ["POST", "PUT", "PATCH", "DELETE"]


class SecurityAuditMiddleware(MiddlewareMixin):
    """
    安全审计中间件

    功能:
    1. 记录敏感路径的访问
    2. 记录认证相关操作
    3. 记录权限变更操作
    4. 检测可疑活动
    """

    def __init__(self, get_response: Callable):
        super().__init__(get_response)
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        # 记录审计前检查（用于登录成功/失败记录）
        request._audit_auth_success = False
        request._audit_auth_user = None

        # 处理请求
        response = self.get_response(request)

        # 审计处理
        self._audit_request(request, response)

        return response

    def _audit_request(self, request: HttpRequest, response: HttpResponse) -> None:
        """审计请求"""
        # 检查是否需要审计
        if not self._should_audit(request):
            return

        try:
            # 获取用户信息
            user_id = getattr(request.user, "id", None)
            username = getattr(request.user, "username", None)

            # 确定事件类型
            event_type = self._get_event_type(request)

            # 记录审计日志
            logger.info(
                f"Security audit: {event_type}",
                extra={
                    "extra_data": {
                        "event_type": event_type,
                        "path": request.path,
                        "method": request.method,
                        "user_id": user_id,
                        "username": username,
                        "status_code": response.status_code,
                        "ip_address": self._get_client_ip(request),
                        "user_agent": request.headers.get("User-Agent", "-")[:200],
                    }
                },
            )
        except Exception:
            pass

    def _should_audit(self, request: HttpRequest) -> bool:
        """检查是否需要审计"""
        # 审计所有 POST/PUT/PATCH/DELETE 请求
        if request.method in AUDIT_METHODS:
            return True

        # 审计特定路径的 GET 请求
        if request.method == "GET":
            for path in AUDIT_PATHS:
                if request.path.startswith(path):
                    return True

        return False

    def _get_event_type(self, request: HttpRequest) -> str:
        """获取事件类型"""
        path = request.path
        method = request.method

        # 认证相关
        if "/login/" in path:
            return "login_attempt"
        if "/logout/" in path:
            return "logout"
        if "/register/" in path:
            return "register"

        # 管理后台
        if path.startswith("/admin/"):
            if method == "POST":
                return "admin_create"
            elif method == "PUT" or method == "PATCH":
                return "admin_update"
            elif method == "DELETE":
                return "admin_delete"
            return "admin_access"

        # 用户管理
        if "/users/" in path:
            if method == "POST":
                return "user_create"
            elif method == "PUT" or method == "PATCH":
                return "user_update"
            elif method == "DELETE":
                return "user_delete"

        # 默认
        return "api_access"

    def _get_client_ip(self, request: HttpRequest) -> str:
        """获取客户端 IP"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "-")


class SuspiciousActivityMiddleware(MiddlewareMixin):
    """
    可疑活动检测中间件

    检测暴力破解、异常访问等可疑行为
    """

    # 检测阈值
    FAILED_LOGIN_THRESHOLD = 5  # 5次失败尝试
    FAILED_LOGIN_WINDOW = 300  # 5分钟窗口

    def __init__(self, get_response: Callable):
        super().__init__(get_response)
        self.get_response = get_response
        self._failed_logins = {}  # {ip: [(timestamp, username), ...]}

    def __call__(self, request: HttpRequest) -> HttpResponse:
        response = self.get_response(request)
        return response

    def process_request(self, request: HttpRequest) -> Optional[HttpResponse]:
        """处理请求前的检查"""
        # 检查登录失败次数
        if "/login/" in request.path and request.method == "POST":
            self._check_failed_logins(request)

        return None

    def _check_failed_logins(self, request: HttpRequest) -> None:
        """检查登录失败次数"""
        ip = self._get_client_ip(request)
        now = now_time = __import__("time").time()

        # 清理过期记录
        self._cleanup_expired(now)

        # 获取用户尝试登录的用户名
        # 注意：这里无法获取认证状态，需要在视图层处理

    def _cleanup_expired(self, now: float) -> None:
        """清理过期记录"""
        expired_ips = []
        for ip, attempts in self._failed_logins.items():
            # 保留5分钟内的记录
            filtered = [(t, u) for t, u in attempts if now - t < self.FAILED_LOGIN_WINDOW]
            if filtered:
                self._failed_logins[ip] = filtered
            else:
                expired_ips.append(ip)

        for ip in expired_ips:
            del self._failed_logins[ip]

    def _get_client_ip(self, request: HttpRequest) -> str:
        """获取客户端 IP"""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR", "-")

    def record_failed_login(self, request: HttpRequest, username: str = None) -> None:
        """记录登录失败（由视图调用）"""
        ip = self._get_client_ip(request)
        now = __import__("time").time()

        if ip not in self._failed_logins:
            self._failed_logins[ip] = []

        self._failed_logins[ip].append((now, username))

        # 检查是否超出阈值
        recent_attempts = [
            (t, u) for t, u in self._failed_logins[ip] if now - t < self.FAILED_LOGIN_WINDOW
        ]

        if len(recent_attempts) >= self.FAILED_LOGIN_THRESHOLD:
            logger.warning(
                "Suspicious activity: multiple failed login attempts",
                extra={
                    "extra_data": {
                        "event_type": "brute_force_attempt",
                        "ip_address": ip,
                        "failed_attempts": len(recent_attempts),
                        "target_username": username,
                        "threshold": self.FAILED_LOGIN_THRESHOLD,
                    }
                },
            )

            # 清理
            self._failed_logins[ip] = []
