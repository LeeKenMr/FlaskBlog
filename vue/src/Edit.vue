<template>
    <div>
        <div class="mx-auto grid max-w-7xl grid-cols-1 gap-10 px-6 lg:grid-cols-12 lg:gap-8 lg:px-8">

            <div class="w-full max-w-md lg:col-span-5 lg:pt-2">
                <div class="flex gap-x-4">
                    <input type="number" v-model="wzid"
                        class="bg-transparent min-w-0 flex-auto rounded-md border-0 px-3.5 py-2 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                        placeholder="输入文章ID">
                    <button type="button" @click="getwz"
                        class="flex-none rounded-md bg-indigo-600 px-3.5 py-2.5 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">拉取文章</button>
                </div>
            </div>
        </div>
    </div>
    <div class="lg:grid lg:grid-cols-2 lg:gap-x-12 xl:gap-x-16">
        <div>
            <div id="tabs-1-panel-1" class="-m-0.5 rounded-lg p-0.5" aria-labelledby="tabs-1-tab-1" role="tabpanel"
                tabindex="0">
                <textarea rows="40" :value="input" @input="update"
                    class="block w-full rounded-md border-0 py-1.5 text-gray-500 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                    placeholder="请输入markdown"></textarea>
            </div>

            <div class="flex justify-between">
                <div class="flex-initial"><button type="button" @click="del"
                        class="inline-flex items-center rounded-md bg-orange-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-orange-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2">删除</button>
                </div>
                <div class="flex-initial">
                    <div class="justify-end">
                        <select v-model="type"
                            class="mr-5 rounded-md border-0 pl-3 pr-10  ring-1 ring-inset ring-gray-300 focus:ring-2 focus:ring-indigo-600 sm:text-sm sm:leading-6">
                            <option value="go">Golang</option>
                            <option value="py">Python</option>
                            <option value="qd">前端</option>
                            <option value="db">数据库</option>
                            <option value="uni">uni-app</option>
                            <option value="ser">运维部署</option>
                            <option value="ai">人工智能</option>
                            <option value="chain">区块链</option>
                            <option value="tools">工具</option>
                        </select>
                        <button type="button" @click="save"
                            class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">保存</button>
                    </div>
                </div>
            </div>
        </div>

        <div v-html="mhtml" class="markedwon text-gray-500"></div>
    </div>
</template>

<script setup>
import { marked } from 'marked'; // markdown解析
import { ref,inject,computed,onMounted } from 'vue'; // vue3
import Prism from 'prismjs'; // 代码高亮

const axios = inject('axios'); //axios

const type = ref(null); //文章类型
const wzid = ref(null); //文章ID
//输入框
const input = ref('');

const getwz = () => {
    if (wzid.value==null || wzid.value=='' || wzid.value==0) {
        alert('请输入文章ID');
        return;
    }
    axios.get('/getwz?id='+wzid.value).then(res => {
        input.value = res.data.markdown;
        type.value = res.data.type;
    }).catch(err => {
        alert('获取文章失败:' + err.data);
    });
};

//提交文章
const save = () => {
    //判断是否填写
    if (!input.value || !type.value || !wzid.value) {
        alert('文章id,内容和类型必填');
        return;
    }
    //取标题
    let biaoti = getBiaoti();
    if (!biaoti) {
        alert('文章没有标题');
        return;
    }
    //提交
    axios.post('/edit', {
        id: wzid.value,
        title: biaoti,
        content: mhtml.value,
        markdown: input.value,
        type: type.value
    }).then(res => {
        alert('保存成功:' + res.data.msg);
    }).catch(err => {
        alert('保存失败:' + err.data);
    });
};

//删除文章
const del = () => {
    //判断是否填写
    if (!wzid.value) {
        alert('文章id为空');
        return;
    }
    //提交
    axios.post('/del', {
        id: wzid.value,
    }).then(res => {
        alert('删除成功:' + res.data.msg);
        //跳转到首页
        window.location.href = '/admin';
    }).catch(err => {
        alert('删除失败:' + err.data);
    });
};

// 获取第一个 <h1>标题
const getBiaoti = () => {
    // 创建一个自定义的 marked.Renderer 实例
    const renderer = new marked.Renderer();
    let h1 = ''; //如果不为空则代表已经获取到h1标签
    // 重写 heading 方法来捕获h标签，方法每遇到一个标题标签就会被调用一次
    renderer.heading = function (text) {
        // 如果是h1标签且h1不为空
       if (text.depth === 1 && !h1) {
              // 如果是h1标签则复制给biaoti变量
              h1 = text.text;
       };
    };
    // 调用自定义的 marked.Renderer去解析
    marked(input.value, { renderer });
    return h1
};

const mhtml = computed(() => {
  // 将 Markdown 转换为 HTML
  const html = marked(input.value,{ breaks: true });
  // 创建一个临时的 DOM 元素
  const tempDiv = document.createElement('div');
  tempDiv.innerHTML = html;
  // 对 HTML 进行语法高亮
  tempDiv.querySelectorAll('pre code').forEach((block) => {
    Prism.highlightElement(block);
  });
    // 返回高亮后的 HTML
  return tempDiv.innerHTML;
});

//更新input触发
const update = (e) => {
    input.value = e.target.value;
};

onMounted(() => {
    Prism.highlightAll();
  });
</script>
<style>
.markedwon h1 {
    font-weight: 550;
    font-size: 1.6em;
}

.markedwon h2 {
    font-weight: 550;
    font-size: 1.4em;
}

.markedwon h3 {
    font-weight: 550;
    font-size: 1.2em;
}

.markedwon h4 {
    font-weight: 550;
    font-size: 1em;
}

.markedwon a {
    color: rgb(53, 101, 233);
}

.markedwon ul li {
    list-style-type: disc;
    margin-left: 1.5em;
}

/* p标签间距，排除blockquote下的p标签 */
.markedwon p:not(blockquote p) {
    margin-top: 1em;
    margin-bottom: 1em;
}

/* > 的样式 */
.markedwon blockquote {
    margin-top: 1em;
    margin-bottom: 1em;
    margin-right: 1em;
    padding-left: 1em;
    padding-top: 4px;
    padding-bottom: 4px;
    border-left: 3px solid rgb(182, 204, 241);
    background-color: rgb(230, 230, 230);
}


/* 自定义` `的样式 */
.markedwon code:not(pre code) {
    display: inline-flex;
    align-items: center;
    border-radius: 0.375rem;
    background-color: rgb(236, 240, 247);
    padding-left: 0.25rem;
    padding-right: 0.25rem;
    padding-top: 0.2rem;
    padding-bottom: 0.2rem;
    margin-left: 0.3rem;
    margin-right: 0.3rem;
    font-size: 14px;
    line-height: 1rem;
    font-weight: 500;
    color: rgb(75 85 99 / var(--tw-text-opacity));
}
/* 设置代码块的样式 */
.markedwon pre {
  border-radius: 0.8rem; /* 设置圆角 */
}
</style>
