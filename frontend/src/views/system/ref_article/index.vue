<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="文章名称" prop="articleName">
        <el-input
          v-model="queryParams.articleName"
          placeholder="请输入文章名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="文献id" prop="refId">
        <el-input
          v-model="queryParams.refId"
          placeholder="请输入文献id"
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
          v-hasPermi="['system:ref_article:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:ref_article:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['system:ref_article:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['system:ref_article:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="ref_articleList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="文章id" align="center" prop="articleId" />
      <el-table-column label="文章名称" align="center" prop="articleName" />
      <el-table-column label="文献id" align="center" prop="refId" />
      <el-table-column label="文章内容" align="center" prop="articleContent" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['system:ref_article:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['system:ref_article:remove']">删除</el-button>
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

    <!-- 添加或修改文献分析对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="ref_articleRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="文章名称" prop="articleName">
        <el-input v-model="form.articleName" placeholder="请输入文章名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="文献id" prop="refId">
        <el-input v-model="form.refId" placeholder="请输入文献id" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="文章内容" prop="articleContent">
        <editor v-model="form.articleContent" :min-height="192"/>
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

<script setup name="Ref_article">
import { listRef_article, getRef_article, delRef_article, addRef_article, updateRef_article } from "@/api/system/ref_article";

const { proxy } = getCurrentInstance();

const ref_articleList = ref([]);
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
    articleName: null,
    refId: null,
    articleContent: null,
  },
  rules: {
    articleName: [
      { required: true, message: "文章名称不能为空", trigger: "blur" }
    ],
    refId: [
      { required: true, message: "文献id不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询文献分析列表 */
function getList() {
  loading.value = true;
  listRef_article(queryParams.value).then(response => {
    ref_articleList.value = response.rows;
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
    articleId: null,
    articleName: null,
    refId: null,
    articleContent: null,
    createBy: null,
    createTime: null,
    updateBy: null,
    updateTime: null,
  };
  proxy.resetForm("ref_articleRef");
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
  ids.value = selection.map(item => item.articleId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加文献分析";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _articleId = row.articleId || ids.value;
  getRef_article(_articleId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改文献分析";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["ref_articleRef"].validate(valid => {
    if (valid) {
      if (form.value.articleId != null) {
        updateRef_article(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addRef_article(form.value).then(response => {
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
  const _articleIds = row.articleId || ids.value;
  proxy.$modal.confirm('是否确认删除文献分析编号为"' + _articleIds + '"的数据项？').then(function() {
    return delRef_article(_articleIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('system/ref_article/export', {
    ...queryParams.value
  }, `ref_article_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.articleId == null ? insert : edit;
}

getList();
</script>