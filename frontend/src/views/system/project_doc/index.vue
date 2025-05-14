<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="文档名称" prop="docName">
        <el-input
          v-model="queryParams.docName"
          placeholder="请输入文档名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="文献id" prop="projectId">
        <el-input
          v-model="queryParams.projectId"
          placeholder="请输入文献id"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="文档简介" prop="docDesc">
        <el-input
          v-model="queryParams.docDesc"
          placeholder="请输入文档简介"
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
          v-hasPermi="['system:project_doc:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:project_doc:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['system:project_doc:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['system:project_doc:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="project_docList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="文档id" align="center" prop="docId" />
      <el-table-column label="文档名称" align="center" prop="docName" />
      <el-table-column label="文献id" align="center" prop="projectId" />
      <el-table-column label="文档简介" align="center" prop="docDesc" />
      <el-table-column label="文档内容" align="center" prop="docContent" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['system:project_doc:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['system:project_doc:remove']">删除</el-button>
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

    <!-- 添加或修改项目文档对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="project_docRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="文档名称" prop="docName">
        <el-input v-model="form.docName" placeholder="请输入文档名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="文献id" prop="projectId">
        <el-input v-model="form.projectId" placeholder="请输入文献id" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="文档简介" prop="docDesc">
        <el-input v-model="form.docDesc" placeholder="请输入文档简介" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="文档内容" prop="docContent">
        <editor v-model="form.docContent" :min-height="192"/>
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

<script setup name="Project_doc">
import { listProject_doc, getProject_doc, delProject_doc, addProject_doc, updateProject_doc } from "@/api/system/project_doc";

const { proxy } = getCurrentInstance();

const project_docList = ref([]);
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
    docName: null,
    projectId: null,
    docDesc: null,
    docContent: null,
  },
  rules: {
    docName: [
      { required: true, message: "文档名称不能为空", trigger: "blur" }
    ],
    projectId: [
      { required: true, message: "文献id不能为空", trigger: "blur" }
    ],
    docDesc: [
      { required: true, message: "文档简介不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询项目文档列表 */
function getList() {
  loading.value = true;
  listProject_doc(queryParams.value).then(response => {
    project_docList.value = response.rows;
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
    docId: null,
    docName: null,
    projectId: null,
    docDesc: null,
    docContent: null,
    createBy: null,
    createTime: null,
    updateBy: null,
    updateTime: null,
  };
  proxy.resetForm("project_docRef");
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
  ids.value = selection.map(item => item.docId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加项目文档";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _docId = row.docId || ids.value;
  getProject_doc(_docId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改项目文档";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["project_docRef"].validate(valid => {
    if (valid) {
      if (form.value.docId != null) {
        updateProject_doc(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addProject_doc(form.value).then(response => {
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
  const _docIds = row.docId || ids.value;
  proxy.$modal.confirm('是否确认删除项目文档编号为"' + _docIds + '"的数据项？').then(function() {
    return delProject_doc(_docIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('system/project_doc/export', {
    ...queryParams.value
  }, `project_doc_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.docId == null ? insert : edit;
}

getList();
</script>