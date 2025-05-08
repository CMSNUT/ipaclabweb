<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="仪器名称" prop="instrumentName">
        <el-input
          v-model="queryParams.instrumentName"
          placeholder="请输入仪器名称"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="功能简介" prop="instrumentRemark">
        <el-input
          v-model="queryParams.instrumentRemark"
          placeholder="请输入功能简介"
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
          v-hasPermi="['system:instrument:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:instrument:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['system:instrument:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['system:instrument:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="instrumentList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="仪器ID" align="center" prop="instrumentId" />
      <el-table-column label="仪器名称" align="center" prop="instrumentName" />
      <el-table-column label="仪器型号" align="center" prop="instrumentModel" />
      <el-table-column label="存放位置" align="center" prop="instrumentRoom" />
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['system:instrument:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['system:instrument:remove']">删除</el-button>
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

    <!-- 添加或修改仪器信息对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="instrumentRef" :model="form" :rules="rules" label-width="80px">
      <el-form-item v-if="renderField(true, true)" label="仪器名称" prop="instrumentName">
        <el-input v-model="form.instrumentName" placeholder="请输入仪器名称" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="仪器型号" prop="instrumentModel">
        <el-input v-model="form.instrumentModel" placeholder="请输入仪器型号" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="功能简介" prop="instrumentRemark">
        <el-input v-model="form.instrumentRemark" placeholder="请输入功能简介" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="存放位置" prop="instrumentRoom">
        <el-input v-model="form.instrumentRoom" placeholder="请输入存放位置" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="图片地址" prop="instrumentImg">
        <image-upload v-model="form.instrumentImg"/>
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

<script setup name="Instrument">
import { listInstrument, getInstrument, delInstrument, addInstrument, updateInstrument } from "@/api/system/instrument";

const { proxy } = getCurrentInstance();

const instrumentList = ref([]);
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
    instrumentName: null,
    instrumentRemark: null,
  },
  rules: {
    instrumentName: [
      { required: true, message: "仪器名称不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询仪器信息列表 */
function getList() {
  loading.value = true;
  listInstrument(queryParams.value).then(response => {
    instrumentList.value = response.rows;
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
    instrumentId: null,
    instrumentName: null,
    instrumentModel: null,
    instrumentRemark: null,
    instrumentRoom: null,
    instrumentImg: null,
    createBy: null,
    createTime: null,
    updateBy: null,
    updateTime: null,
  };
  proxy.resetForm("instrumentRef");
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
  ids.value = selection.map(item => item.instrumentId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加仪器信息";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _instrumentId = row.instrumentId || ids.value;
  getInstrument(_instrumentId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改仪器信息";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["instrumentRef"].validate(valid => {
    if (valid) {
      if (form.value.instrumentId != null) {
        updateInstrument(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addInstrument(form.value).then(response => {
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
  const _instrumentIds = row.instrumentId || ids.value;
  proxy.$modal.confirm('是否确认删除仪器信息编号为"' + _instrumentIds + '"的数据项？').then(function() {
    return delInstrument(_instrumentIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('system/instrument/export', {
    ...queryParams.value
  }, `instrument_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.instrumentId == null ? insert : edit;
}

getList();
</script>