<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="标签名称" prop="tagLabel">
        <el-input
          v-model="queryParams.tagLabel"
          placeholder="请输入标签名称"
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
          v-hasPermi="['resource:tag:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="info"
          plain
          icon="Sort"
          @click="toggleExpandAll"
        >展开/折叠</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table
      v-if="refreshTable"
      v-loading="loading"
      :data="tagList"
      row-key="tagId"
      :default-expand-all="isExpandAll"
      :tree-props="{children: 'children', hasChildren: 'hasChildren'}"
    >
      <el-table-column label="标签名称" align="center" prop="tagLabel" />
      <el-table-column label="标签值" align="center" prop="tagValue" />
      <el-table-column label="父标签" align="center" prop="parentId" >
        <template #default="scope">
          <span>{{ getParentTagLabel(scope.row.parentId) || 'null' }}</span>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['resource:tag:edit']">修改</el-button>
          <el-button link type="primary" icon="Plus" @click="handleAdd(scope.row)" v-hasPermi="['${moduleName}:${businessName}:add']">新增</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['resource:tag:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 添加或修改标签管理对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="tagRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="标签名称" prop="tagLabel">
        <el-input v-model="form.tagLabel" placeholder="请输入标签名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="标签值" prop="tagValue">
        <el-input v-model="form.tagValue" placeholder="请输入标签值" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="父标签id" prop="parentId">
        <el-tree-select
          v-model="form.parentId"
          :data="tagOptions"
          :props="{ value: 'tagId', label: 'tagLabel', children: 'children' }"
          value-key="tagId"
          placeholder="请选择父标签id"
          check-strictly
        />
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

<script setup name="Tag">
import { listTag, getTag, delTag, addTag, updateTag } from "@/api/resource/tag";

const { proxy } = getCurrentInstance();

const tagList = ref([]);
const tagOptions = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const title = ref("");
const isExpandAll = ref(true);
const refreshTable = ref(true);
// 标签ID到名称的映射表
const tagMap = ref(new Map());

const data = reactive({
  form: {},
  queryParams: {
    tagLabel: null,
  },
  rules: {
    tagLabel: [
      { required: true, message: "标签名称不能为空", trigger: "blur" }
    ],
    tagValue: [
      { required: true, message: "标签值不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询标签管理列表 */
function getList() {
  loading.value = true;
  listTag(queryParams.value).then(response => {
    tagList.value = proxy.handleTree(response.data, "tagId", "parentId");
    // 建立ID到名称的映射，提高查找效率
    tagMap.value = new Map(
      response.data.map(tag => [tag.tagId, tag.tagLabel])
    );
    loading.value = false;
  });
}

/** 获取父标签的名称 */
const getParentTagLabel = (parentId) => {
  if (!parentId) return ''; // 顶级标签
  return tagMap.value.get(parentId) || '未知标签' ;
}

/** 查询标签管理下拉树结构 */
function getTreeselect() {
  listTag().then(response => {
    tagOptions.value = [];
    const data = { tagId: 0, tagLabel: '顶级节点', children: [] };
    data.children = proxy.handleTree(response.data, "tagId", "parentId");
    tagOptions.value.push(data);
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
    tagId: null,
    tagLabel: null,
    tagValue: null,
    parentId: null,
    createBy: null,
    createTime: null,
    updateBy: null,
    updateTime: null,
  };
  proxy.resetForm("tagRef");
}

/** 搜索按钮操作 */
function handleQuery() {
  getList();
}

/** 重置按钮操作 */
function resetQuery() {
  proxy.resetForm("queryRef");
  handleQuery();
}

/** 新增按钮操作 */
function handleAdd(row) {
  reset();
  getTreeselect();
  if (row != null && row.tagId) {
    form.value.parentId = row.tagId;
  } else {
    form.value.parentId = 0;
  }
  open.value = true;
  title.value = "添加标签管理";
}

/** 展开/折叠操作 */
function toggleExpandAll() {
  refreshTable.value = false;
  isExpandAll.value = !isExpandAll.value;
  nextTick(() => {
    refreshTable.value = true;
  });
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  getTreeselect();
  if (row != null) {
    form.value.parentId = row.parentId;
  }
  getTag(row.tagId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改标签管理";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["tagRef"].validate(valid => {
    if (valid) {
      if (form.value.tagId != null) {
        updateTag(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addTag(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除标签管理编号为"' + row.tagId + '"的数据项？').then(function() {
    return delTag(row.tagId);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.tagId == null ? insert : edit;
}

getList();
</script>