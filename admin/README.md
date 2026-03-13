# Admin Frontend Guide

## 配置划分

`admin/` 目录现在按两类配置使用：

- 开发配置：本地 `vite dev server` 使用，重点是代理后端 API
- 部署配置：生产构建使用，重点是 API 基地址和构建产物行为

公共逻辑在 `src/config/env.ts`，Vite 按 `mode` 读取环境变量，配置入口在 `vite.config.ts`。

## 环境变量

### 开发环境

复制示例文件：

```bash
cd admin
cp .env.development.example .env.development
```

推荐值：

```env
VITE_API_BASE_URL=
VITE_DEV_PROXY_TARGET=http://localhost:9999
VITE_BUILD_SOURCEMAP=false
```

说明：

- `VITE_API_BASE_URL`
  开发时建议留空，前端直接请求 `/api/...`，由 Vite 代理到 Django
- `VITE_DEV_PROXY_TARGET`
  本地 Django 服务地址，默认是 `http://localhost:9999`
- `VITE_BUILD_SOURCEMAP`
  仅控制构建输出 sourcemap，开发阶段通常保持 `false`

### 生产环境

复制示例文件：

```bash
cd admin
cp .env.production.example .env.production
```

推荐值：

```env
VITE_API_BASE_URL=
VITE_DEV_PROXY_TARGET=http://localhost:9999
VITE_BUILD_SOURCEMAP=false
```

说明：

- 生产环境推荐 `VITE_API_BASE_URL=` 留空
  因为 `console.liangbax.com` 下的 `/api/` 由 Nginx 反代到 Django，前端保持同源请求最简单
- `VITE_DEV_PROXY_TARGET` 在生产构建里不会参与运行时请求，只是保留默认值，方便本地构建复用同一套配置

## 使用方式

### 本地开发

确保 Django 本地运行在 `http://localhost:9999`，然后执行：

```bash
cd admin
npm ci
npm run dev:local
```

开发时这些路径会自动代理到 Django：

- `/api`
- `/media`
- `/documents`
- `/static`

### 本地构建

```bash
cd admin
npm run build
```

或者显式指定生产模式：

```bash
cd admin
npm run build:prod
```

构建产物输出到 `admin/dist/`。

### 生产部署

当前生产方案是：

- 前端构建产物部署到服务器的 `frontend_dist/`
- `console.liangbax.com` 由 Nginx 静态托管前端
- `console.liangbax.com/api/`、`/media/`、`/documents/` 反代到 Django

因此生产环境通常不需要把 API 域名写成绝对地址，保持 `VITE_API_BASE_URL=` 即可。

## 配置约定

- 开发代理配置只放在 `vite.config.ts`
- 运行时 API 地址只从 `src/config/env.ts` 读取
- 业务代码里不要直接写 `localhost`、部署域名或新的 `import.meta.env.VITE_*`
- 如果后续新增部署变量，先补到：
  - `src/vite-env.d.ts`
  - `src/config/env.ts`
  - `.env.*.example`

## 常见问题

### 为什么开发环境推荐 `VITE_API_BASE_URL=` 留空

因为这样所有请求都是相对路径，浏览器访问 `http://localhost:5173` 时由 Vite 代理到 Django，切到生产后仍然是同样的请求路径，不需要改业务代码。

### 什么时候需要设置绝对 API 地址

只有在前端不再通过 Nginx 反代 `/api/`，而是要直接请求另一个域名时，才需要把 `VITE_API_BASE_URL` 配成完整地址，例如：

```env
VITE_API_BASE_URL=https://liangbax.com
```
