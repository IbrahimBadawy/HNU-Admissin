import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite';

export default defineConfig({
    plugins: [
        vue(),
        VueI18nPlugin({
            include: path.resolve(__dirname, './src/locales/**'),
        }),
    ],
    resolve: {
        alias: {
            '@': path.resolve(__dirname, './src'),
        },
    },
    optimizeDeps: {
        include: ['quill'],
    },
    server: {
        host: true,
        port: 5173,
        allowedHosts: ['admission.hnu.edu.eg','localhost'], // 👈 ده المهم
      },
});
