# JWT 认证系统实现说明

## 概述

本项目已将后台管理系统的登录认证方式从 Django Session 认证升级为 JWT (JSON Web Token) 认证。

## 主要改进

### 后端改进

1. **添加 JWT 依赖**
   - 在 `requirements.txt` 中添加了 `djangorestframework-simplejwt==5.3.1`

2. **配置 JWT 认证**
   - 在 `base_settings.py` 中：
     - 添加 `rest_framework_simplejwt` 到 `INSTALLED_APPS`
     - 配置 `REST_FRAMEWORK` 使用 `JWTAuthentication`
     - 添加 `SIMPLE_JWT` 配置，包括：
       - Access Token 有效期：60分钟
       - Refresh Token 有效期：7天
       - 启用 Token 轮换和黑名单机制

3. **更新登录视图**
   - 在 `apps/admin_api/views.py` 中：
     - 移除 Django session 认证（`login`, `logout`）
     - 使用 `RefreshToken.for_user(user)` 生成 JWT token
     - 返回 `access` 和 `refresh` 两个 token
     - 添加管理员权限检查（`is_staff`）

4. **创建用户信息视图**
   - 在 `apps/admin_api/views.py` 中新增 `UserInfoView`：
     - 独立的用户信息获取视图
     - 从数据库重新获取用户信息，确保数据最新
     - 使用 `IsAuthenticated` 权限类

5. **添加 Token 刷新端点**
   - 在 `apps/admin_api/urls.py` 中添加 `/auth/refresh/` 端点

### 前端改进

1. **更新类型定义**
   - 在 `admin/src/types/index.ts` 中：
     - `LoginResponse` 从 `{ token, user }` 改为 `{ access, refresh, user }`

2. **更新 API 接口**
   - 在 `admin/src/api/auth.ts` 中：
     - 添加 `refreshToken` 函数用于刷新 token

3. **优化请求拦截器**
   - 在 `admin/src/utils/request.ts` 中：
     - 移除 `withCredentials: true`（不再使用 cookie）
     - 使用 `admin_access_token` 和 `admin_refresh_token` 存储键名
     - 实现 Token 自动刷新机制：
       - 当收到 401 错误时，自动使用 refresh token 获取新的 access token
       - 使用队列机制处理并发请求，避免重复刷新
       - 刷新失败时自动清除认证信息并跳转登录页

4. **更新状态管理**
   - 在 `admin/src/store/useAuthStore.ts` 中：
     - 将 `token` 改为 `accessToken` 和 `refreshToken`
     - 添加 `setTokens` 方法同时设置两个 token

5. **更新认证 Hook**
   - 在 `admin/src/hooks/useAuth.ts` 中：
     - 登录时同时存储 access token 和 refresh token
     - 退出时清除所有 token
     - 添加 `refreshUserInfo` 方法用于刷新用户信息
     - 保持向后兼容（`token` 属性指向 `accessToken`）

## 使用方法

### 安装依赖

```bash
pip install djangorestframework-simplejwt==5.3.1
```

### 后端配置

JWT 配置已在 `base_settings.py` 中完成，主要配置如下：

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
}
```

### 前端使用

登录流程保持不变，JWT token 会自动处理：

```typescript
import { useAuth } from '@/hooks/useAuth';

const { login, logout, isAuthenticated, refreshUserInfo } = useAuth();

// 登录
await login({ username, password });

// 退出
await logout();

// 刷新用户信息（获取最新用户状态）
const latestUser = await refreshUserInfo();
```

### 获取最新用户信息

系统提供了专门的接口来获取最新的用户信息：

**后端接口**：`GET /api/admin/auth/me/`

- 需要认证（携带有效的 JWT token）
- 从数据库重新获取用户信息，确保数据是最新的
- 返回完整的用户信息

**前端使用**：

```typescript
import { useAuth } from '@/hooks/useAuth';

const { refreshUserInfo } = useAuth();

// 在需要获取最新用户信息时调用
const latestUser = await refreshUserInfo();
if (latestUser) {
  console.log('最新用户信息:', latestUser);
}
```

**使用场景**：
- 用户修改个人信息后刷新显示
- 检查用户权限是否发生变化
- 定期同步用户状态

## Token 机制说明

### Access Token
- **用途**：用于 API 请求认证
- **有效期**：60分钟
- **存储位置**：localStorage (`admin_access_token`)
- **使用方式**：在请求头中添加 `Authorization: Bearer {access_token}`

### Refresh Token
- **用途**：用于获取新的 access token
- **有效期**：7天
- **存储位置**：localStorage (`admin_refresh_token`)
- **使用方式**：调用 `/api/admin/auth/refresh/` 接口

### Token 自动刷新

前端实现了智能的 token 自动刷新机制：

1. 当 API 请求返回 401 错误时，自动触发 token 刷新
2. 使用 refresh token 获取新的 access token
3. 如果有多个并发请求，只发送一次刷新请求，其他请求排队等待
4. 刷新成功后，自动重试所有失败的请求
5. 刷新失败时，清除认证信息并跳转登录页

## 安全特性

1. **Token 轮换**：每次刷新 token 时，会生成新的 refresh token，旧的 refresh token 会被加入黑名单
2. **管理员权限检查**：只有 `is_staff=True` 的用户才能登录后台管理系统
3. **Token 过期处理**：access token 过期后自动刷新，refresh token 过期后需要重新登录
4. **无状态认证**：不再依赖 session，支持分布式部署

## 迁移说明

### 数据库迁移

如果需要使用 token 黑名单功能，需要运行以下命令：

```bash
python manage.py migrate
```

### 兼容性

- 前端代码保持向后兼容，`useAuth()` 返回的 `token` 属性指向 `accessToken`
- 现有的登录页面代码无需修改
- 所有 API 请求会自动携带 JWT token

## 测试建议

1. 测试正常登录流程
2. 测试 token 过期后的自动刷新
3. 测试并发请求时的 token 刷新
4. 测试 refresh token 过期后的处理
5. 测试非管理员用户登录（应返回 403 错误）

## 常见问题

### Q: Token 存储在 localStorage 是否安全？
A: 对于后台管理系统，localStorage 是可接受的方案。如果需要更高的安全性，可以考虑使用 httpOnly cookie 存储 refresh token。

### Q: 如何修改 token 有效期？
A: 在 `base_settings.py` 的 `SIMPLE_JWT` 配置中修改 `ACCESS_TOKEN_LIFETIME` 和 `REFRESH_TOKEN_LIFETIME`。

### Q: 如何实现单点登录？
A: 可以在登录时生成唯一的 session ID，并在 token 中包含该 ID。每次请求时验证 session ID 是否有效。

### Q: Token 刷新失败怎么办？
A: 前端会自动清除认证信息并跳转登录页，用户需要重新登录。

## 相关文件

### 后端
- `requirements.txt` - JWT 依赖
- `base_settings.py` - JWT 配置
- `apps/admin_api/views.py` - 登录视图、用户信息视图
- `apps/admin_api/urls.py` - 路由配置

### 前端
- `admin/src/types/index.ts` - 类型定义
- `admin/src/api/auth.ts` - API 接口
- `admin/src/utils/request.ts` - 请求拦截器
- `admin/src/store/useAuthStore.ts` - 状态管理
- `admin/src/hooks/useAuth.ts` - 认证 Hook
