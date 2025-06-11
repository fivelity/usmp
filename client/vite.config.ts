import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig, loadEnv } from "vite";
import path from "path";
import tailwindcss from "tailwindcss";
import autoprefixer from "autoprefixer";

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), "");

  const apiTarget =
    env.API_PROXY_TARGET || env.VITE_API_BASE_URL || "http://localhost:8100";

  return {
    plugins: [sveltekit()],
    server: {
      port: 5501,
      host: "0.0.0.0",
      proxy: {
        "/api": {
          target: apiTarget,
          changeOrigin: true,
        },
        "/ws": {
          target: apiTarget.replace(/^http/, "ws"),
          ws: true,
          changeOrigin: true,
        },
      },
    },
    build: {
      target: "esnext",
      minify: "esbuild",
      sourcemap: false,
      rollupOptions: {
        output: {
          manualChunks: {
            vendor: ["svelte"],
          },
        },
      },
    },
    optimizeDeps: {
      include: ["@lucide/svelte"],
    },
    define: {
      // Suppress Node.js deprecation warnings in browser
      "process.env.NODE_ENV": JSON.stringify(
        process.env.NODE_ENV || "development",
      ),
    },
    resolve: {
      alias: {
        $lib: path.resolve("./src/lib"),
      },
    },
    css: {
      postcss: {
        plugins: [tailwindcss, autoprefixer],
      },
    },
  };
});
