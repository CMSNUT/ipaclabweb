<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="教程名称" prop="tutorialName">
        <el-input
          v-model="queryParams.tutorialName"
          placeholder="请输入教程名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="算法id" prop="algoId">
        <el-input
          v-model="queryParams.algoId"
          placeholder="请输入算法id"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
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
          v-hasPermi="['system:algo_tutorial:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:algo_tutorial:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['system:algo_tutorial:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['system:algo_tutorial:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="algo_tutorialList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="教程id" align="center" prop="tutorialId" />
      <el-table-column label="教程名称" align="center" prop="tutorialName" />
      <el-table-column label="算法id" align="center" prop="algoId" />
      <el-table-column label="教程内容" align="center" prop="tutorialContent" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['system:algo_tutorial:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['system:algo_tutorial:remove']">删除</el-button>
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

    <!-- 添加或修改算法教程对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="algo_tutorialRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="教程名称" prop="tutorialName">
        <el-input v-model="form.tutorialName" placeholder="请输入教程名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="算法id" prop="algoId">
        <el-input v-model="form.algoId" placeholder="请输入算法id" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="教程内容" prop="tutorialContent">
        <editor v-model="form.tutorialContent" :min-height="192"/>
      </el-form-item>

      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button type="primary" @click="submitForm">确 定</el-button>
          <el-button @click="cancel">取 消</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="Algo_tutorial">
import { listAlgo_tutorial, getAlgo_tutorial, delAlgo_tutorial, addAlgo_tutorial, updateAlgo_tutorial } from "@/api/system/algo_tutorial";

const { proxy } = getCurrentInstance();

const algo_tutorialList = ref([]);
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
    tutorialName: null,
    algoId: null,
    tutorialContent: null,
  },
  rules: {
    tutorialName: [
      { required: true, message: "教程名称不能为空", trigger: "blur" }
    ],
    algoId: [
      { required: true, message: "算法id不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询算法教程列表 */
function getList() {
  loading.value = true;
  listAlgo_tutorial(queryParams.value).then(response => {
    algo_tutorialList.value = response.rows;
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
    tutorialId: null,
    tutorialName: null,
    algoId: null,
    tutorialContent: null,
    createBy: null,
    createTime: null,
    updateBy: null,
    updateTime: null,
  };
  proxy.resetForm("algo_tutorialRef");
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
  ids.value = selection.map(item => item.tutorialId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加算法教程";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _tutorialId = row.tutorialId || ids.value;
  getAlgo_tutorial(_tutorialId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改算法教程";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["algo_tutorialRef"].validate(valid => {
    if (valid) {
      if (form.value.tutorialId != null) {
        updateAlgo_tutorial(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addAlgo_tutorial(form.value).then(response => {
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
  const _tutorialIds = row.tutorialId || ids.value;
  proxy.$modal.confirm('是否确认删除算法教程编号为"' + _tutorialIds + '"的数据项？').then(function() {
    return delAlgo_tutorial(_tutorialIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('system/algo_tutorial/export', {
    ...queryParams.value
  }, `algo_tutorial_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.tutorialId == null ? insert : edit;
}

getList();
</script>