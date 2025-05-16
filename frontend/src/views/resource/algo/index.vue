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
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="algoRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="程序名称" prop="algoName">
        <el-input v-model="form.algoName" placeholder="请输入程序名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="程序介绍" prop="algoDesc">
        <editor v-model="form.algoDesc" :min-height="192"/>
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

<script setup name="Algo">
import { listAlgo, getAlgo, delAlgo, addAlgo, updateAlgo } from "@/api/resource/algo";

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