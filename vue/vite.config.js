import { fileURLToPath, URL } from 'node:url'
import { prismjsPlugin } from 'vite-plugin-prismjs'; //语法高亮插件
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    vue(),
    prismjsPlugin({
      languages: ['markup', 'css', 'javascript','go','json','python','sql','shell'], // 语言
      plugins: ['line-numbers'], //官网有其他功能:https://prismjs.com/#plugins
      theme: 'default', // 主题
      css: true,
  }),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  build: {
    assetsDir: 'static', // assets文件改为static
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1',
        changeOrigin: true,
      }
    },
    host: '127.0.0.1'
  }
})


