import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios';
import { message } from 'antd';

// Token 存储键名
const ACCESS_TOKEN_KEY = 'admin_access_token';
const REFRESH_TOKEN_KEY = 'admin_refresh_token';

// 是否正在刷新 token
let isRefreshing = false;
// 存储待重试的请求
let failedQueue: Array<{
	resolve: (value: any) => void;
	reject: (reason?: any) => void;
}> = [];

// 处理队列中的请求
const processQueue = (error: any, token: string | null = null) => {
	failedQueue.forEach((prom) => {
		if (error) {
			prom.reject(error);
		} else {
			prom.resolve(token);
		}
	});
	failedQueue = [];
};

// 创建 axios 实例
const request = axios.create({
	timeout: 30000,
	headers: {
		'Content-Type': 'application/json',
	},
});

// 请求拦截器
request.interceptors.request.use(
	(config: InternalAxiosRequestConfig) => {
		// 从 localStorage 获取 access token
		const token = localStorage.getItem(ACCESS_TOKEN_KEY);
		if (token && config.headers) {
			config.headers.Authorization = `Bearer ${token}`;
		}
		return config;
	},
	(error: AxiosError) => {
		return Promise.reject(error);
	},
);

// 响应拦截器
request.interceptors.response.use(
	(response) => {
		const res = response.data;
		if (response.status === 200 || response.status === 201) {
			return res;
		}
		// DELETE 请求返回 204 No Content 时，res 为空但请求成功
		if (response.status === 204) {
			return { status: 'success' };
		}
		message.error(res?.message || '请求失败');
		return Promise.reject(new Error(res?.message || '请求失败'));
	},
	async (error: AxiosError) => {
		const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean };

		if (error.response) {
			const status = error.response.status;

			// Token 过期，尝试刷新
			if (status === 401 && originalRequest && !originalRequest._retry) {
				if (isRefreshing) {
					// 如果正在刷新，将请求加入队列
					return new Promise((resolve, reject) => {
						failedQueue.push({ resolve, reject });
					})
						.then((token) => {
							if (originalRequest.headers) {
								originalRequest.headers.Authorization = `Bearer ${token}`;
							}
							return request(originalRequest);
						})
						.catch((err) => {
							return Promise.reject(err);
						});
				}

				originalRequest._retry = true;
				isRefreshing = true;

				const refreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);

				if (!refreshToken) {
					// 没有 refresh token，直接跳转登录
					clearAuth();
					return Promise.reject(error);
				}

				try {
					// 调用刷新 token 接口
					const response = await axios.post('/api/admin/auth/refresh/', {
						refresh: refreshToken,
					});

					const { access, refresh } = response.data;

					// 更新存储的 token
					localStorage.setItem(ACCESS_TOKEN_KEY, access);
					if (refresh) {
						localStorage.setItem(REFRESH_TOKEN_KEY, refresh);
					}

					// 处理队列中的请求
					processQueue(null, access);

					// 重试原请求
					if (originalRequest.headers) {
						originalRequest.headers.Authorization = `Bearer ${access}`;
					}
					return request(originalRequest);
				} catch (refreshError) {
					// 刷新失败，清除认证信息并跳转登录
					processQueue(refreshError, null);
					clearAuth();
					return Promise.reject(refreshError);
				} finally {
					isRefreshing = false;
				}
			}

			// 其他错误处理
			switch (status) {
				case 401:
					message.error('登录已过期，请重新登录');
					clearAuth();
					break;
				case 403:
					message.error('没有权限访问');
					break;
				case 404:
					message.error('请求的资源不存在');
					break;
				case 500:
					message.error('服务器错误');
					break;
				default:
					message.error(
						(error.response.data as any)?.detail || (error.response.data as any)?.message || '请求失败',
					);
			}
		} else if (error.request) {
			message.error('网络连接失败，请检查网络');
		} else {
			message.error('请求配置错误');
		}
		return Promise.reject(error);
	},
);

// 清除认证信息
const clearAuth = () => {
	localStorage.removeItem(ACCESS_TOKEN_KEY);
	localStorage.removeItem(REFRESH_TOKEN_KEY);
	localStorage.removeItem('admin_user');
	window.location.href = '/login';
};

export default request;
