<template>
  <!-- 编辑器容器，添加灰色边框 -->
  <div style="border: 1px solid #ccc">
    <!-- 工具栏组件 -->

    <!-- style 工具栏底部边框
      :editor 绑定编辑器实例
      :defaultConfig 工具栏配置
      :mode 模式 default/simple -->

    <Toolbar style="border-bottom: 1px solid #ccc" :editor="editorRef" :defaultConfig="toolbarConfig" :mode="mode" />

    <!-- 编辑器组件 -->

    <!-- style 固定高度，隐藏纵向滚动条
      v-model 双向绑定编辑器内容
      :defaultConfig 编辑器配置
      :mode  模式 default/simple
      @onCreated 创建完成回调 -->

    <!-- https://segmentfault.com/a/1190000042722618 -->
    <Editor 
      :style="editorStyle"
      v-model="valueHtml" 
      :defaultConfig="editorConfig" 
      :mode="mode"
      @onCreated="handleCreated" 
      @onChange="handleChange" />
  </div>
</template>

<script setup>
// 引入编辑器样式（重要！否则样式不生效）
import '@wangeditor/editor/dist/css/style.css'

// Vue相关依赖
import { onBeforeUnmount, ref, shallowRef, onMounted, getCurrentInstance } from 'vue'
// 编辑器组件
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'

import axios from 'axios'
import { getToken } from "@/utils/auth";

const { proxy } = getCurrentInstance();
const uploadUrl = ref(import.meta.env.VITE_APP_BASE_API + "/common/upload"); // 上传的图片服务器地址
const headers = ref({
  Authorization: "Bearer " + getToken()
});

// 编辑器实例必须用 shallowRef（性能优化，避免深层响应）
const editorRef = shallowRef()

// 使用 ref 创建响应式的 HTML 内容
const valueHtml = ref('')

const emits = defineEmits(['update:modelValue'])

const props = defineProps({
  /* 编辑器的内容 */
  modelValue: {
    type: String,
  },
  /* 高度 */
  height: {
    type: Number,
    default: null,
  },
  /* 最小高度 */
  minHeight: {
    type: Number,
    default: null,
  },
  /* 只读 */
  readOnly: {
    type: Boolean,
    default: false,
  },
  /* 上传文件大小限制(MB) */
  fileSize: {
    type: Number,
    default: 5,
  },
  /* 类型（base64格式、url格式） */
  type: {
    type: String,
    default: "url",
  }
});

// 动态计算编辑器样式
const editorStyle = computed(() => ({
  height: props.height ? `${props.height}px` : '300px',
  minHeight: props.minHeight ? `${props.minHeight}px` : 'auto',
  overflowY: 'hidden'
}));

watch(() => props.modelValue, (v) => {
  if (v !== valueHtml.value) {
    valueHtml.value = v == undefined ? "<p></p>" : v;
  }
}, { immediate: true });

watch(valueHtml, (val) => {
  emits('update:modelValue', val);
});

// 工具栏配置（空对象表示使用默认配置）
const toolbarConfig = {}

// 编辑器配置（设置占位提示文字）
const editorConfig = {
  placeholder: '请输入内容...', // 配置默认提示
  MENU_CONF: {                // 配置上传服务器地址
    uploadImage: {
      base64LimitSize: 5 * 1024 * 1024, // 5M
      allowedFileTypes: ['image/*'],
    }
  }
}

// 编辑器模式：default（完整）或 simple（简洁）
const mode = 'default'

// 编辑器创建完成回调
const handleCreated = (editor) => {
  editorRef.value = editor  // 存储编辑器实例
}

// 监听只读状态
watch(() => props.readOnly, (readOnly) => {
  const editor = editorRef.value;
  if (editor) readOnly ? editor.disable() : editor.enable();
});

// 组件销毁前，销毁编辑器实例（防止内存泄漏）
onBeforeUnmount(() => {
  const editor = editorRef.value
  if (editor == null) return
  editor.destroy()
})
</script>
