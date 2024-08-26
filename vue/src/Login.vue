!<template>
    <main class="sm:px-12 py-6 space-x-3 text-gray-800">

        <div class="flex min-h-full flex-col justify-center px-6 py-12 lg:px-8">
            <div class="sm:mx-auto sm:w-full sm:max-w-sm">
                今天也要努力
            </div>

            <div class="mt-10 sm:mx-auto sm:w-full sm:max-w-sm">
                <form class="space-y-6" :model="loginuser">
                    <div>
                        <label for="name" class="block text-sm font-medium leading-6">账户</label>
                        <div class="mt-2">
                            <input type="text" v-model="loginuser.name"
                                class="block w-full rounded-md border-0 py-1.5 bg-transparent ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
                        </div>
                    </div>

                    <div>
                        <label for="password" class="block text-sm font-medium leading-6">密码</label>
                        <div class="mt-2">
                            <input type="password" v-model="loginuser.password"
                                class="block w-full rounded-md border-0 py-1.5 bg-transparent ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6">
                        </div>
                    </div>

                    <div>
                        <button type="button" @click="login"
                            class="flex w-full justify-center rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-semibold leading-6 text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">登录</button>
                    </div>
                </form>

            </div>
            <!-- 通知信息 -->
            <div class="sm:mx-auto rounded-md bg-yellow-50 p-4 mt-5" v-if="msg !=''">
                <div class="flex">
                    <div class="flex-shrink-0 pt-2">
                        <svg class="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                            <path fill-rule="evenodd"
                                d="M8.485 2.495c.673-1.167 2.357-1.167 3.03 0l6.28 10.875c.673 1.167-.17 2.625-1.516 2.625H3.72c-1.347 0-2.189-1.458-1.515-2.625L8.485 2.495zM10 5a.75.75 0 01.75.75v3.5a.75.75 0 01-1.5 0v-3.5A.75.75 0 0110 5zm0 9a1 1 0 100-2 1 1 0 000 2z"
                                clip-rule="evenodd" />
                        </svg>
                    </div>
                    <div class="ml-3">
                        <div class="mt-2 text-sm text-yellow-700">
                            <p>{{ msg }}</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
    </main>
</template>

<script setup>
import { ref,inject } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();
const axios = inject("axios");
const msg = ref('');
const loginuser = ref({
    name: '',
    password: ''
});
//登录事件
const login = () => {
    //判断是否为空
    if (!loginuser.value.name || !loginuser.value.password) {
        msg.value = '账户或密码不能为空';
        return;
    }
    axios.post('/login', loginuser.value)
        .then(res => {
            //保存token
            localStorage.setItem('token', res.data.token);
            //跳转到admin首页
            router.push({ path: '/admin' });
        })
        .catch(err => {
            msg.value = err.response.data.msg;
        })
};
</script>
