!<template>
    <button type="button" @click="sitemap"
    class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">更新sitemap</button>
</template>

<script setup>
import { inject } from 'vue';
const axios = inject('axios');
const sitemap = () => {
    axios.get('/sitemap').then(res => {
        alert('更新成功:' + res.data.msg);
    }).catch(err => {
        alert('更新失败:' + err.data);
    });
};
</script>
