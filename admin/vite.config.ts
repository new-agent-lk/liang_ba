import { defineConfig, loadEnv } from "vite";
import react from "@vitejs/plugin-react";
import path from "path";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");
  const devProxyTarget = env.VITE_DEV_PROXY_TARGET || "http://localhost:9999";
  const isProduction = mode === "production";

  return {
    base: "/",
    plugins: [react()],
    resolve: {
      alias: {
        "@": path.resolve(__dirname, "./src"),
      },
    },
    server: {
      host: "0.0.0.0",
      port: 5173,
      proxy: {
        "/api": {
          target: devProxyTarget,
          changeOrigin: true,
        },
        "/media": {
          target: devProxyTarget,
          changeOrigin: true,
        },
        "/documents": {
          target: devProxyTarget,
          changeOrigin: true,
        },
        "/static": {
          target: devProxyTarget,
          changeOrigin: true,
        },
      },
    },
    build: {
      outDir: "dist",
      sourcemap: env.VITE_BUILD_SOURCEMAP === "true",
      rollupOptions: {
        output: {
          chunkFileNames: "assets/js/[name]-[hash].js",
          entryFileNames: "assets/js/[name]-[hash].js",
          assetFileNames: "assets/[ext]/[name]-[hash].[ext]",
          manualChunks: {
            vendor: ["react", "react-dom", "react-router-dom"],
            antd: ["antd", "@ant-design/icons"],
            echarts: ["echarts", "echarts-for-react"],
          },
        },
      },
      ...(isProduction
        ? {}
        : {
            minify: false,
          }),
    },
  };
});
