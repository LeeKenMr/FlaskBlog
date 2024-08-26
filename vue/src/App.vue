<template>
  <!-- 这是管理员后台 -->
  <div class="text-gray-500 bg-gray-100">
      <nav class="border-b border-gray-900/15">
          <!-- 移动隐藏侧栏导航 -->
          <div v-show="openMenu" class="relative z-50 sm:hidden" role="dialog" aria-modal="true">

              <div class="fixed inset-0 bg-white/80"></div>

              <div class="fixed inset-0 flex w-full max-w-xs">

                  <div class="relative mr-16 flex flex-1">

                      <div class="absolute left-full top-0 flex w-16 justify-center pt-5">
                          <button @click="openMenu = false" type="button"
                              class="-m-2.5 p-2.5 rounded-lg px-3 py-1.5 shadow-none hover:bg-gray-100">
                              <!-- 关闭按钮 -->
                              <svg class="h-6 w-6 text-black" fill="none" viewBox="0 0 24 24"
                                  stroke-width="1.5" stroke="currentColor" aria-hidden="true">
                                  <path stroke-linecap="round" stroke-linejoin="round" d="M6 18L18 6M6 6l12 12" />
                              </svg>
                          </button>
                      </div>
                      <div
                          class="flex grow flex-col gap-y-5 overflow-y-auto bg-gray-200 px-6 pb-4 ring-1 ring-white/10">
                          <nav class="flex flex-1 flex-col">
                              <ul role="list" class="flex flex-1 flex-col gap-y-7 pt-3">
                                  <li>
                                      <ul role="list" class="-mx-2 space-y-1">
                                          <li>
                                              <router-link :to="'/admin'" @click="openMenu = false"
                                                  class="hover:bg-slate-400 group flex gap-x-3 rounded-md p-2 text-sm leading-6">
                                                  返回首页
                                              </router-link>
                                          </li>
                                          <li>
                                               <router-link :to="'/admin/add'" @click="openMenu = false"
                                                  class="hover:bg-slate-400 group flex gap-x-3 rounded-md p-2 text-sm leading-6">
                                                  写文章
                                                </router-link>
                                          </li>
                                          <li>
                                                <router-link :to="'/admin/edit'" @click="openMenu = false"
                                                  class="hover:bg-slate-400 group flex gap-x-3 rounded-md p-2 text-sm leading-6">
                                                  改文章
                                                </router-link>
                                          </li>
                                          <li>
                                                <button @click="logout"
                                                  class="hover:bg-slate-400 group flex gap-x-3 rounded-md p-2 text-sm leading-6">
                                                  注销
                                                </button>
                                          </li>
                                          
                                      </ul>
                                  </li>
                                  
                              </ul>
                          </nav>
                      </div>
                  </div>
              </div>
          </div>

          <!-- 桌面导航开始 -->
          <div class="sm:block hidden mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-3">
              <div class="flex justify-between sm:space-x-6">
                  <!-- 导航左下分类栏 -->
                  <div class="flex flex-1 items-center justify-center sm:items-stretch sm:justify-start">
                      <div class="sm:ml-6 sm:flex sm:space-x-8">
                        <router-link :to="'/admin'"
                        class="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium hover:border-gray-300">返回首页</router-link>
                        <router-link :to="'/admin/add'" class="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium hover:border-gray-300">写文章</router-link>
                        <router-link :to="'/admin/edit'"
                              class="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium hover:border-gray-300">改文章</router-link>
                        <button @click="logout"
                              class="inline-flex items-center border-b-2 border-transparent px-1 pt-1 text-sm font-medium hover:border-gray-300">注销</button>
                      </div>
                  </div>
                  
              </div>
          </div>

          <!-- 下面是移动导航 -->
          <div class="sm:hidden flex mx-auto justify-between pt-2">
              <div class="inline-flex inset-y-0 right-0 items-center">
                  <!-- 折叠按钮 -->
                  <div class="inset-y-0 left-0 flex items-end">
                      <button @click="openMenu = true" type="button"
                          class="relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-gray-100 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-indigo-500"
                          aria-controls="mobile-menu" aria-expanded="false">
                          <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
                              stroke="currentColor" aria-hidden="true">
                              <path stroke-linecap="round" stroke-linejoin="round"
                                  d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
                          </svg>
                      </button>
                  </div>

              </div>
          </div>



      </nav>
  </div>

  <div class="bg-gray-100 min-h-lvh">
      <div class="mx-auto max-w-7xl">
          <router-view></router-view>
      </div>
  </div>
  <footer class="my-10 text-center">------------已经到底了-----------</footer>

</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const openMenu = ref(false); // 是否显示移动端菜单
// 注销登录
const logout = () => {
    localStorage.removeItem("token");
    router.push("/admin/login");
    openMenu.value = false;
}
</script>