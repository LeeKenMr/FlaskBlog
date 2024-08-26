import { createRouter,createWebHistory } from "vue-router";

import Login from "./Login.vue";
import Index from "./Index.vue";
import Add from "./Add.vue";
import Edit from "./Edit.vue";

const routes = [ //指定路由
    {path:"/admin/login",component:Login},
    {path:"/admin",component:Index},
    {path:"/admin/add",component:Add},
    {path:"/admin/edit",component:Edit},
];

const router = createRouter({ //创建路由
    history: createWebHistory(), //路由模式
    routes, //路由，由之前的数组变量作为参数
});

export default router //返回这个路由被调用