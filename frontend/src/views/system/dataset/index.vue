<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="数据名称" prop="datasetName">
        <el-input
          v-model="queryParams.datasetName"
          placeholder="请输入数据名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="数据简介" prop="datasetDesc">
        <el-input
          v-model="queryParams.datasetDesc"
          placeholder="请输入数据简介"
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
          v-hasPermi="['system:dataset:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:dataset:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['system:dataset:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['system:dataset:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="datasetList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="数据id" align="center" prop="datasetId" />
      <el-table-column label="数据名称" align="center" prop="datasetName" />
      <el-table-column label="数据简介" align="center" prop="datasetDesc" />
      <el-table-column label="数据详情" align="center" prop="datasetContent" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['system:dataset:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['system:dataset:remove']">删除</el-button>
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

    <!-- 添加或修改数据管理对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="datasetRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="数据名称" prop="datasetName">
        <el-input v-model="form.datasetName" placeholder="请输入数据名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="数据简介" prop="datasetDesc">
        <el-input v-model="form.datasetDesc" placeholder="请输入数据简介" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="数据详情" prop="datasetContent">
        <editor v-model="form.datasetContent" :min-height="192"/>
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

<script setup name="Dataset">
import { listDataset, getDataset, delDataset, addDataset, updateDataset } from "@/api/system/dataset";

const { proxy } = getCurrentInstance();

const datasetList = ref([]);
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
    datasetName: null,
    datasetDesc: null,
    datasetContent: null,
  },
  rules: {
    datasetName: [
      { required: true, message: "数据名称不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询数据管理列表 */
function getList() {
  loading.value = true;
  listDataset(queryParams.value).then(response => {
    datasetList.value = response.rows;
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
    datasetId: null,
    datasetName: null,
    datasetDesc: null,
    datasetContent: null,
    createBy: null,
    createTime: null,
    updateBy: null,
    updateTime: null,
  };
  proxy.resetForm("datasetRef");
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
  ids.value = selection.map(item => item.datasetId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加数据管理";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _datasetId = row.datasetId || ids.value;
  getDataset(_datasetId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改数据管理";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["datasetRef"].validate(valid => {
    if (valid) {
      if (form.value.datasetId != null) {
        updateDataset(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addDataset(form.value).then(response => {
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
  const _datasetIds = row.datasetId || ids.value;
  proxy.$modal.confirm('是否确认删除数据管理编号为"' + _datasetIds + '"的数据项？').then(function() {
    return delDataset(_datasetIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('system/dataset/export', {
    ...queryParams.value
  }, `dataset_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.datasetId == null ? insert : edit;
}

getList();
</script>