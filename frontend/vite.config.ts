import { defineConfig } from 'vite';
import vue from '@vitejs/plugin-vue';
import path from 'path';
import VueI18nPlugin from '@intlify/unplugin-vue-i18n/vite';
import Components from 'unplugin-vue-components/vite';
import { PrimeVueResolver } from '@primevue/auto-import-resolver';
import fs from 'fs';

export default defineConfig({
    plugins: [
        vue(),
        VueI18nPlugin({
            include: path.resolve(__dirname, './src/locales/**'),
        }),
        Components({
            resolvers: [PrimeVueResolver()],
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
        https: {
            key: fs.readFileSync('C:/nginx/conf/ssl/admission_hnu_edu_eg.key'),
            cert: fs.readFileSync('C:/nginx/conf/ssl/admission_hnu_edu_eg.crt'),
            ca: fs.readFileSync('C:/nginx/conf/ssl/SSL_COM_ROOT_CERTIFICATION_AUTHORITY_RSA.crt'),
          },
        allowedHosts: ['admission.hnu.edu.eg','pay.hnu.edu.eg','193.227.34.93', 'localhost'],
        proxy: {
            '/api': {
                target: 'https://admission.hnu.edu.eg',
                // target: 'http://admission.hnu.edu.eg',
                // target: 'http://193.227.34.93',
                // target: 'http://pay.hnu.edu.eg',
                changeOrigin: true,
            },
        }, // 👈 ده المهم
    },
});
