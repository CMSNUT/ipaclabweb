<template>
  <div class="editor-wrapper">
    <div ref="editorContainer" class="editor-container"></div>
    
    <!-- 图片上传按钮 -->
    <div class="editor-actions">
      <el-upload
        class="editor-upload-btn"
        :action="uploadUrl"
        :headers="uploadHeaders"
        :on-success="handleUploadSuccess"
        :before-upload="beforeUpload"
        :show-file-list="false"
        accept="image/*"
      >
        <el-button type="primary" size="small">上传图片</el-button>
      </el-upload>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch, defineProps, defineEmits } from 'vue';
import Quill from 'quill';
import 'quill/dist/quill.snow.css';
import axios from 'axios';

// 导入图片处理模块
import { extractImageUrls, getRelativePath } from '@/utils/image-utils';

// 定义属性和事件
const props = defineProps({
  modelValue: {
    type: String,
    default: ''
  },
  height: {
    type: [String, Number],
    default: '300px'
  },
  uploadUrl: {
    type: String,
    default: '/api/upload/image'
  },
  deleteUrl: {
    type: String,
    default: '/api/delete/image'
  }
});

const emits = defineEmits(['update:modelValue', 'change', 'focus', 'blur']);

// 引用和状态
const editorContainer = ref(null);
const quillEditor = ref(null);
const isEditorReady = ref(false);
const initialContent = ref('');
const currentImages = ref(new Set()); // 当前内容中的图片URL
const deletedImages = ref([]); // 已删除的图片URL

// 获取上传请求头（包含认证信息）
const uploadHeaders = computed(() => {
  const token = localStorage.getItem('token');
  return token ? { Authorization: `Bearer ${token}` } : {};
});

// 初始化编辑器
onMounted(() => {
  nextTick(() => {
    // 配置Quill编辑器
    const options = {
      theme: 'snow',
      modules: {
        toolbar: [
          ['bold', 'italic', 'underline', 'strike'],
          ['blockquote', 'code-block'],
          [{ header: 1 }, { header: 2 }],
          [{ list: 'ordered' }, { list: 'bullet' }],
          [{ script: 'sub' }, { script: 'super' }],
          [{ indent: '-1' }, { indent: '+1' }],
          [{ direction: 'rtl' }],
          [{ size: ['small', false, 'large', 'huge'] }],
          [{ header: [1, 2, 3, 4, 5, 6, false] }],
          [{ color: [] }, { background: [] }],
          [{ font: [] }],
          [{ align: [] }],
          ['clean'],
          ['link', 'image', 'video']
        ]
      },
      placeholder: '请输入内容...',
      bounds: editorContainer.value,
      scrollingContainer: 'body'
    };
    
    // 创建编辑器实例
    quillEditor.value = new Quill(editorContainer.value, options);
    
    // 设置初始内容
    if (props.modelValue) {
      quillEditor.value.setContents(JSON.parse(props.modelValue));
      initialContent.value = props.modelValue;
    }
    
    // 记录初始图片
    currentImages.value = extractImageUrls(props.modelValue);
    
    // 监听内容变化
    quillEditor.value.on('text-change', (delta, oldDelta, source) => {
      if (source === 'user') {
        const content = quillEditor.value.getContents();
        const contentJson = JSON.stringify(content);
        
        // 触发内容更新事件
        emits('update:modelValue', contentJson);
        emits('change', contentJson);
        
        // 检测图片删除
        checkForDeletedImages(contentJson);
      }
    });
    
    // 监听焦点事件
    quillEditor.value.on('selection-change', (range) => {
      if (range) {
        emits('focus');
      } else {
        emits('blur');
      }
    });
    
    isEditorReady.value = true;
  });
});

// 监听外部内容变化
watch(() => props.modelValue, (newValue) => {
  if (isEditorReady.value && newValue !== JSON.stringify(quillEditor.value.getContents())) {
    quillEditor.value.setContents(JSON.parse(newValue));
    currentImages.value = extractImageUrls(newValue);
  }
});

// 检测删除的图片
function checkForDeletedImages(content) {
  const newImages = extractImageUrls(content);
  const removedImages = [...currentImages.value].filter(url => !newImages.has(url));
  
  if (removedImages.length > 0) {
    // 记录已删除的图片
    removedImages.forEach(url => {
      if (!deletedImages.value.includes(url)) {
        deletedImages.value.push(url);
      }
    });
    
    // 提示用户并删除服务器上的图片
    confirmDeleteImages(removedImages);
  }
  
  // 更新当前图片集合
  currentImages.value = newImages;
}

// 确认删除图片
function confirmDeleteImages(imageUrls) {
  if (imageUrls.length === 0) return;
  
  // 显示确认对话框
  proxy.$modal.confirm(`确定要删除${imageUrls.length}张图片吗？删除后无法恢复。`).then(() => {
    // 逐个删除服务器上的图片
    imageUrls.forEach(url => {
      deleteImageFromServer(url);
    });
  }).catch(() => {
    // 用户取消删除，恢复图片
    restoreDeletedImages(imageUrls);
  });
}

// 从服务器删除图片
function deleteImageFromServer(url) {
  // 提取图片在服务器上的相对路径
  const imagePath = getRelativePath(url);
  if (!imagePath) return;
  
  // 调用API删除图片
  axios.delete(props.deleteUrl, {
    data: { path: imagePath },
    headers: uploadHeaders.value
  })
  .then(() => {
    proxy.$message.success('图片删除成功');
  })
  .catch(error => {
    proxy.$message.error(`图片删除失败: ${error.message}`);
  });
}

// 恢复已删除的图片
function restoreDeletedImages(imageUrls) {
  // 从deletedImages中移除这些URL
  deletedImages.value = deletedImages.value.filter(url => !imageUrls.includes(url));
  
  // 如果编辑器已初始化，恢复内容中的图片
  if (quillEditor.value) {
    const content = quillEditor.value.getContents();
    const contentJson = JSON.stringify(content);
    
    // 简单地将图片添加回内容中（实际实现可能需要更复杂的处理）
    let newContent = contentJson;
    imageUrls.forEach(url => {
      const imgHtml = `<img src="${url}" alt="恢复的图片" />`;
      // 这里只是简单地添加到内容末尾，实际可能需要更智能的处理
      newContent = newContent.replace('</p>', `${imgHtml}</p>`);
    });
    
    // 更新编辑器内容
    quillEditor.value.setContents(JSON.parse(newContent));
    emits('update:modelValue', newContent);
    emits('change', newContent);
    
    // 更新当前图片集合
    currentImages.value = extractImageUrls(newContent);
  }
}

// 处理图片上传成功
function handleUploadSuccess(response, file) {
  // 直接使用axios上传文件
  const formData = new FormData();
  formData.append('file', file);
  
  axios.post(props.uploadUrl, formData, {
    headers: {
      ...uploadHeaders.value,
      'Content-Type': 'multipart/form-data'
    }
  })
  .then(response => {
    if (response.data.code === 200 && response.data.data.url) {
      // 获取图片URL
      const imageUrl = response.data.data.url;
      
      // 将图片插入到编辑器中
      if (quillEditor.value) {
        const range = quillEditor.value.getSelection();
        quillEditor.value.insertEmbed(range.index, 'image', imageUrl);
        quillEditor.value.setSelection(range.index + 1);
        
        // 更新当前图片集合
        currentImages.value.add(imageUrl);
      }
    } else {
      proxy.$message.error('图片上传失败');
    }
  })
  .catch(error => {
    proxy.$message.error(`图片上传失败: ${error.message}`);
  });
}

// 上传前处理
function beforeUpload(file) {
  const isJpgOrPng = file.type === 'image/jpeg' || file.type === 'image/png';
  if (!isJpgOrPng) {
    proxy.$message.error('只能上传JPG/PNG格式的图片!');
    return false;
  }
  
  const isLt2M = file.size / 1024 / 1024 < 2;
  if (!isLt2M) {
    proxy.$message.error('图片大小不能超过2MB!');
    return false;
  }
  
  return true;
}

// 清理资源
onBeforeUnmount(() => {
  if (quillEditor.value) {
    quillEditor.value.off('text-change');
    quillEditor.value.off('selection-change');
    quillEditor.value = null;
  }
});

// 获取当前实例代理
const { proxy } = getCurrentInstance();
</script>

<style scoped>
.editor-wrapper {
  position: relative;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.editor-container {
  flex: 1;
  min-height: 150px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  overflow: hidden;
}

.editor-actions {
  margin-top: 10px;
  display: flex;
  justify-content: flex-end;
}

/* 调整Quill编辑器样式 */
.ql-container {
  height: calc(100% - 42px) !important; /* 减去工具栏高度 */
  border: none !important;
}

.ql-toolbar {
  border: none !important;
  border-bottom: 1px solid #ebeef5 !important;
}
</style>