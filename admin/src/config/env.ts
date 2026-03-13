const trimTrailingSlash = (value: string) => value.replace(/\/+$/, "");

const getEnv = (key: keyof ImportMetaEnv, fallback: string) => {
  const value = import.meta.env[key];
  return trimTrailingSlash(value && value.length > 0 ? value : fallback);
};

export const APP_ENV = import.meta.env.MODE;
export const API_BASE_URL = getEnv("VITE_API_BASE_URL", "");
export const DEV_PROXY_TARGET = getEnv(
  "VITE_DEV_PROXY_TARGET",
  "http://localhost:9999",
);
export const APP_BASE_PATH = import.meta.env.BASE_URL || "/";
