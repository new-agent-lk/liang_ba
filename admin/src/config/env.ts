const trimTrailingSlash = (value: string) => value.replace(/\/+$/, "");
const normalizeApiBaseUrl = (value: string) => {
  const trimmed = trimTrailingSlash(value);
  return trimmed === "/api" ? "" : trimmed;
};

const getEnv = (key: keyof ImportMetaEnv, fallback: string) => {
  const value = import.meta.env[key];
  return normalizeApiBaseUrl(value && value.length > 0 ? value : fallback);
};

export const APP_ENV = import.meta.env.MODE;
export const API_BASE_URL = getEnv("VITE_API_BASE_URL", "");
export const APP_BASE_PATH = import.meta.env.BASE_URL || "/";
