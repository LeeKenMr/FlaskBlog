import '../public/static/admin.css';
import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';


const app = createApp(App);
app.use(router) //启用路由;

axios.defaults.baseURL = "/api";
axios.defaults.headers.post['Content-Type'] = 'application/json';
// // 获取 token
// const token = localStorage.getItem('token');

// // 如果 token 存在，设置 Axios 的默认 Authorization 头
// if (token) {
//     axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
// } else {
//     console.log("token不存在");
// }

// 请求请求拦截器
axios.interceptors.request.use(
    config => {
      let token = localStorage.getItem('token');
      console.log('获取到的token:', token);
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
      }
      return config;
    },
    error => {
      return Promise.reject(error);
    }
  );

//响应拦截遇到401错误跳转到登录页面
axios.interceptors.response.use(
    response => response,
    error => {
      if (error.response && error.response.status === 401) {
        // window.location.href = '/admin/login';
        alert('登录过期，请重新登录');
      }
      return Promise.reject(error);
    }
);
app.provide("axios",axios); //全局共享axios

app.mount('#app');