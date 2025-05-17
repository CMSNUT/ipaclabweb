<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="程序名称" prop="algoName">
        <el-input
          v-model="queryParams.algoName"
          placeholder="请输入程序名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="程序类型" prop="algoType">
        <el-select v-model="queryParams.algoType" placeholder="请选择程序类型" clearable style="width: 240px">
          <el-option
            v-for="dict in sys_program_type"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="编程语言" prop="algoLang">
        <el-select v-model="queryParams.algoLang" placeholder="请选择编程语言" clearable style="width: 240px">
          <el-option
            v-for="dict in sys_program_lang"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['resource:algo:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['resource:algo:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['resource:algo:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['resource:algo:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="algoList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="程序ID" align="center" prop="algoId" />
      <el-table-column label="程序名称" align="center" prop="algoName" />
      <el-table-column label="程序介绍" align="center" prop="algoDesc" />
      <el-table-column label="程序类型" align="center" prop="algoType">
        <template #default="scope">
            <dict-tag :options="sys_program_type" :value="scope.row.algoType"/>
        </template>
      </el-table-column>
      <el-table-column label="编程语言" align="center" prop="algoLang">
        <template #default="scope">
            <dict-tag :options="sys_program_lang" :value="scope.row.algoLang"/>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['resource:algo:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['resource:algo:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination
      v-show="total>0"
      :total="total"
      v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize"
      @pagination="getList"
    />

    <!-- 添加或修改程序管理对话框 -->
    <el-dialog 
      :title="title" 
      v-model="open" 
      :width="dialogWidth + 'px'" 
      :draggable="true" 
      append-to-body
      @open="onDialogOpen"
      @resize="onDialogResize"
      class="resizable-dialog"
    >
      <el-form ref="algoRef" :model="form" :rules="rules" label-width="80px" class="dialog-form">
        <el-form-item v-if="renderField(true, true)" label="程序名称" prop="algoName">
          <el-input v-model="form.algoName" placeholder="请输入程序名称" />
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="程序类型" prop="algoType">
          <el-select v-model="form.algoType" placeholder="请选择程序类型">
            <el-option
              v-for="dict in sys_program_type"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="编程语言" prop="algoLang">
          <el-select v-model="form.algoLang" placeholder="请选择编程语言">
            <el-option
              v-for="dict in sys_program_lang"
              :key="dict.value"
              :label="dict.label"
              :value="dict.value"
            ></el-option>
          </el-select>
        </el-form-item>

        <!-- 改进：添加响应式富文本编辑框 -->
        <el-form-item v-if="renderField(true, true)" label="程序介绍" prop="algoDesc">
          <editor 
            ref="editorRef" 
            v-model="form.algoDesc" 
            :height="editorHeight" 
            class="editor-container responsive-editor"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
      
      <!-- 缩放手柄 -->
      <div class="resize-handle" @mousedown="startResize"></div>
      <div class="resize-handle-right" @mousedown="startResizeWidth"></div>
    </el-dialog>
  </div>
</template>

<script setup name="Algo">
import { listAlgo, getAlgo, delAlgo, addAlgo, updateAlgo } from "@/api/resource/algo";
import { ref, computed, onUnmounted, getCurrentInstance, nextTick, watch } from 'vue';

// 对话框尺寸管理
const dialogWidth = ref(500);
const dialogHeight = ref(400);
const MIN_DIALOG_WIDTH = 400;
const MIN_DIALOG_HEIGHT = 350;

// 缩放状态管理
const isResizing = ref(false);
const isResizingWidth = ref(false);
const initialX = ref(0);
const initialY = ref(0);
const initialWidth = ref(0);
const initialHeight = ref(0);

// 富文本编辑框引用和高度计算
const editorRef = ref(null);
const editorHeight = computed(() => {
  // 计算编辑框高度：对话框高度减去其他元素占用的高度
  return Math.max(150, dialogHeight.value - 220); // 220是其他元素的估计高度
});

// 编辑框宽度计算 - 确保始终跟随对话框宽度
const editorWidth = computed(() => {
  // 获取对话框主体宽度减去内边距
  return dialogWidth.value - 40; // 40是对话框内边距的估计值
});

// 缩放处理函数
function startResize(event) {
  isResizing.value = true;
  initialX.value = event.clientX;
  initialY.value = event.clientY;
  initialWidth.value = dialogWidth.value;
  initialHeight.value = dialogHeight.value;
  
  document.addEventListener('mousemove', handleResize);
  document.addEventListener('mouseup', stopResize);
}

function startResizeWidth(event) {
  isResizingWidth.value = true;
  initialX.value = event.clientX;
  initialWidth.value = dialogWidth.value;
  
  document.addEventListener('mousemove', handleResizeWidth);
  document.addEventListener('mouseup', stopResizeWidth);
}

function handleResize(event) {
  if (!isResizing.value) return;
  
  const dx = event.clientX - initialX.value;
  const dy = event.clientY - initialY.value;
  
  dialogWidth.value = Math.max(MIN_DIALOG_WIDTH, initialWidth.value + dx);
  dialogHeight.value = Math.max(MIN_DIALOG_HEIGHT, initialHeight.value + dy);
}

function handleResizeWidth(event) {
  if (!isResizingWidth.value) return;
  
  const dx = event.clientX - initialX.value;
  dialogWidth.value = Math.max(MIN_DIALOG_WIDTH, initialWidth.value + dx);
}

function stopResize() {
  isResizing.value = false;
  document.removeEventListener('mousemove', handleResize);
  document.removeEventListener('mouseup', stopResize);
  updateEditorSize(); // 更新编辑框大小
}

function stopResizeWidth() {
  isResizingWidth.value = false;
  document.removeEventListener('mousemove', handleResizeWidth);
  document.removeEventListener('mouseup', stopResizeWidth);
  updateEditorSize(); // 更新编辑框大小
}

// 更新编辑框大小
function updateEditorSize() {
  nextTick(() => {
    if (editorRef.value) {
      // 强制更新编辑框高度和宽度
      editorRef.value.$el.style.height = `${editorHeight.value}px`;
      editorRef.value.$el.style.width = `${editorWidth.value}px`;
      
      // 查找编辑框内部的内容区域并设置宽度
      const contentArea = editorRef.value.$el.querySelector('.ql-editor') || editorRef.value.$el.querySelector('.editor-content');
      if (contentArea) {
        contentArea.style.width = '100%';
        contentArea.style.maxWidth = 'none';
      }
      
      // 确保编辑器容器没有固定宽度限制
      const editorContainer = editorRef.value.$el;
      if (editorContainer) {
        editorContainer.style.maxWidth = 'none';
        editorContainer.style.width = '100%';
      }
    }
  });
}

// 对话框事件处理
function onDialogOpen() {
  // 对话框打开时初始化大小
  nextTick(() => {
    const dialog = document.querySelector('.resizable-dialog .el-dialog');
    if (dialog) {
      dialogWidth.value = dialog.offsetWidth;
      dialogHeight.value = dialog.offsetHeight;
      updateEditorSize();
      
      // 添加对话框尺寸变化的观察器
      observeDialogSize(dialog);
    }
  });
}

function onDialogResize() {
  // 对话框大小改变时更新编辑框大小
  nextTick(() => {
    const dialog = document.querySelector('.resizable-dialog .el-dialog');
    if (dialog) {
      dialogWidth.value = dialog.offsetWidth;
      dialogHeight.value = dialog.offsetHeight;
      updateEditorSize();
    }
  });
}

// 对话框尺寸变化观察器
let resizeObserver = null;
function observeDialogSize(element) {
  // 清除之前的观察器
  if (resizeObserver) {
    resizeObserver.disconnect();
  }
  
  // 创建新的观察器
  resizeObserver = new ResizeObserver(entries => {
    for (let entry of entries) {
      dialogWidth.value = entry.contentRect.width;
      dialogHeight.value = entry.contentRect.height;
      updateEditorSize();
    }
  });
  
  // 开始观察
  resizeObserver.observe(element);
}

// 生命周期钩子
onUnmounted(() => {
  document.removeEventListener('mousemove', handleResize);
  document.removeEventListener('mouseup', stopResize);
  document.removeEventListener('mousemove', handleResizeWidth);
  document.removeEventListener('mouseup', stopResizeWidth);
  
  // 断开观察器连接
  if (resizeObserver) {
    resizeObserver.disconnect();
    resizeObserver = null;
  }
});

// 监听对话框高度变化，实时更新编辑框大小
watch(dialogHeight, () => {
  updateEditorSize();
});

// 监听对话框宽度变化，实时更新编辑框大小
watch(dialogWidth, () => {
  updateEditorSize();
});

const { proxy } = getCurrentInstance();
const { sys_program_type, sys_program_lang } = proxy.useDict('sys_program_type', 'sys_program_lang');

const algoList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    algoName: null,
    algoDesc: null,
    algoType: null,
    algoLang: null,
  },
  rules: {
    algoName: [
      { required: true, message: "程序名称不能为空", trigger: "blur" }
    ],
    algoType: [
      { required: true, message: "程序类型不能为空", trigger: "change" }
    ],
    algoLang: [
      { required: true, message: "编程语言不能为空", trigger: "change" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询程序管理列表 */
function getList() {
  loading.value = true;
  listAlgo(queryParams.value).then(response => {
    algoList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 取消按钮 */
function cancel() {
  open.value = false;
  reset();
}

/** 表单重置 */
function reset() {
  form.value = {
    algoId: null,
    algoName: null,
    algoDesc: null,
    algoType: null,
    algoLang: null,
    createBy: null,
    createTime: null,
    updateBy: null,
    updateTime: null,
  };
  proxy.resetForm("algoRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  queryParams.value.pageNum = 1;
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}

/** 多选框选中数据  */
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.algoId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加程序管理";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _algoId = row.algoId || ids.value;
  getAlgo(_algoId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改程序管理";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["algoRef"].validate(valid => {
    if (valid) {
      if (form.value.algoId != null) {
        updateAlgo(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addAlgo(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
function handleDelete(row) {
  const _algoIds = row.algoId || ids.value;
  proxy.$modal.confirm('是否确认删除程序管理编号为"' + _algoIds + '"的数据项？').then(function() {
    return delAlgo(_algoIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}

/** 导出按钮操作 */
function handleExport() {
  proxy.download('resource/algo/export', {
    ...queryParams.value
  }, `algo_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.algoId == null ? insert : edit;
}

getList();
</script>

<style scoped>
/* 缩放手柄样式 */
.resize-handle {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 15px;
  height: 15px;
  cursor: se-resize;
  background-color: #ccc;
  z-index: 10;
}

.resize-handle-right {
  position: absolute;
  right: 0;
  top: 0;
  bottom: 0;
  width: 5px;
  cursor: ew-resize;
  background-color: #f0f0f0;
  z-index: 10;
}

/* 对话框样式 */
.resizable-dialog .el-dialog {
  display: flex;
  flex-direction: column;
  max-height: 90vh;
  overflow: hidden;
}

.resizable-dialog .el-dialog__body {
  flex: 1;
  min-height: 0;
  padding: 20px;
  box-sizing: border-box;
  overflow: hidden;
}

/* 编辑框容器样式 */
.editor-container {
  width: 100%; /* 确保容器宽度占满父容器 */
  height: 100%;
  min-height: 150px;
  box-sizing: border-box;
}

/* 确保编辑框响应式 */
.responsive-editor, .responsive-editor * {
  box-sizing: border-box;
  max-width: 100% !important;
  width: 100% !important;
}

/* 表单布局优化 */
.dialog-form {
  height: 100%;
  display: flex;
  flex-direction: column;
}

.el-form-item:last-child {
  flex: 1;
  min-height: 0;
  display: flex;
  flex-direction: column;
}
</style>