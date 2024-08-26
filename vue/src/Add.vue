<template>
    <div class="lg:grid lg:grid-cols-2 lg:gap-x-12 xl:gap-x-16">
        <div>
                <div id="tabs-1-panel-1" class="-m-0.5 rounded-lg p-0.5" aria-labelledby="tabs-1-tab-1" role="tabpanel"
                    tabindex="0">
                        <textarea rows="40" :value="input" @input="update"
                            class="block w-full rounded-md border-0 py-1.5 text-gray-500 shadow-sm ring-1 ring-inset ring-gray-300 placeholder:text-gray-400 focus:ring-2 focus:ring-inset focus:ring-indigo-600 sm:text-sm sm:leading-6"
                            placeholder="请输入markdown"></textarea>
                </div>
            
            <div class="mt-2 flex justify-end">
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
                <button type="button" @click="add"
                    class="inline-flex items-center rounded-md bg-indigo-600 px-3 py-2 text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600">发表文章</button>
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
//输入框
const input = ref('');


//提交文章
const add = () => {
    //判断是否填写
    if (!input.value || !type.value) {
        alert('内容和类型必填');
        return;
    }
    //取标题
    let biaoti = getBiaoti();
    if (!biaoti) {
        alert('文章没有标题');
        return;
    }
    //提交
    axios.post('/add', {
        title: biaoti,
        content: mhtml.value,
        markdown: input.value,
        type: type.value
    }).then(res => {
        alert('发表成功:' + res.data.msg);
    }).catch(err => {
        alert('发表失败:' + err.data);
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
  const html = marked(input.value,{breaks: true});
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
/* p标签间距，排除blockquote下的p标签 */
.markedwon p:not(blockquote p) {
    margin-top: 1em;
    margin-bottom: 1em;
}

.markedwon ul li {
    list-style-type: disc;
    margin-left: 1.5em;
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
