<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
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
          v-hasPermi="['system:ref:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:ref:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['system:ref:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['system:ref:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="refList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="文献id" align="center" prop="refId" />
      <el-table-column label="文献英文标题" align="center" prop="refTitle" />
      <el-table-column label="文献中文标题" align="center" prop="refTitleZh" />
      <el-table-column label="文献DOI" align="center" prop="refDoi" />
      <el-table-column label="文献摘要" align="center" prop="refAbs" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['system:ref:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['system:ref:remove']">删除</el-button>
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

    <!-- 添加或修改文献管理对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="refRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="文献英文标题" prop="refTitle">
        <el-input v-model="form.refTitle" type="textarea" placeholder="请输入内容" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="文献中文标题" prop="refTitleZh">
        <el-input v-model="form.refTitleZh" type="textarea" placeholder="请输入内容" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="文献DOI" prop="refDoi">
        <el-input v-model="form.refDoi" type="textarea" placeholder="请输入内容" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="文献摘要" prop="refAbs">
        <el-input v-model="form.refAbs" type="textarea" placeholder="请输入内容" />
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

<script setup name="Ref">
import { listRef, getRef, delRef, addRef, updateRef } from "@/api/system/ref";

const { proxy } = getCurrentInstance();

const refList = ref([]);
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
    refTitle: null,
    refTitleZh: null,
    refDoi: null,
    refAbs: null,
  },
  rules: {
    refTitle: [
      { required: true, message: "文献英文标题不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询文献管理列表 */
function getList() {
  loading.value = true;
  listRef(queryParams.value).then(response => {
    refList.value = response.rows;
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
    refId: null,
    refTitle: null,
    refTitleZh: null,
    refDoi: null,
    refAbs: null,
    createBy: null,
    createTime: null,
    updateBy: null,
    updateTime: null,
  };
  proxy.resetForm("refRef");
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
  ids.value = selection.map(item => item.refId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加文献管理";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _refId = row.refId || ids.value;
  getRef(_refId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改文献管理";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["refRef"].validate(valid => {
    if (valid) {
      if (form.value.refId != null) {
        updateRef(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addRef(form.value).then(response => {
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
  const _refIds = row.refId || ids.value;
  proxy.$modal.confirm('是否确认删除文献管理编号为"' + _refIds + '"的数据项？').then(function() {
    return delRef(_refIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('system/ref/export', {
    ...queryParams.value
  }, `ref_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.refId == null ? insert : edit;
}

getList();
</script>