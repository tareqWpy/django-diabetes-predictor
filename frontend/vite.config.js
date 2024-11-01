import vue from "@vitejs/plugin-vue";
import { defineConfig } from "vite";

// https://vite.dev/config/
export default defineConfig(() => {
    return {
        plugins: [vue()],
        define: {
            "process.env.VITE_BACKEND_URL": JSON.stringify(
                process.env.VITE_BACKEND_URL
            ),
        },
        server: {
            host: "0.0.0.0",
            port: 5173,
        },
    };
});
