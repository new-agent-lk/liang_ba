import request from "@/utils/request";
import { LoginParams, LoginResponse, User } from "@/types";

export const login = (data: LoginParams): Promise<LoginResponse> => {
  return request.post("/api/admin/auth/login/", data);
};

export const logout = (): Promise<void> => {
  return request.post("/api/admin/auth/logout/");
};

export const getCurrentUser = (): Promise<User> => {
  return request.get("/api/admin/auth/me/");
};

export const refreshToken = (
  refreshToken: string,
): Promise<{ access: string; refresh: string }> => {
  return request.post("/api/admin/auth/refresh/", { refresh: refreshToken });
};
