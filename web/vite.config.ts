import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Proxy requests starting with /api to backend at localhost:8000
      "/api": "http://localhost:8000",
    },
  },
});
