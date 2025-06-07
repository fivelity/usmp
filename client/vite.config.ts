import { sveltekit } from "@sveltejs/kit/vite";
import { defineConfig } from "vite";
import path from "path";
import tailwindcss from "tailwindcss";
import autoprefixer from "autoprefixer";

export default defineConfig({
  plugins: [sveltekit()],
  server: {
    port: 5501,
    host: "0.0.0.0",
    proxy: {
      "/api": {
        target: "http://localhost:8100",
        changeOrigin: true,
      },
      "/ws": {
        target: "ws://localhost:8100",
        ws: true,
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
});
