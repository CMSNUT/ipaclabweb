<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <el-form-item label="仪器名称" prop="deviceName">
        <el-input v-model="queryParams.deviceName" placeholder="请输入仪器名称" clearable style="width: 240px"
          @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      
      <el-col :span="1.5">
        <el-button type="warning" plain icon="Download" @click="handleExport"
          v-hasPermi="['resource:device:export']">导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="deviceList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="仪器ID" align="center" prop="deviceId" />
      <el-table-column label="仪器名称" align="center" prop="deviceName" />
      <el-table-column label="仪器图片" align="center" prop="deviceImg" width="100">
        <template #default="scope">
          <image-preview :src="scope.row.deviceImg" :width="50" :height="50" />
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize" @pagination="getList" />
  </div>
</template>

<script setup name="Device">
import { listDevice, getDevice, delDevice, addDevice, updateDevice } from "@/api/resource/device";
import axios from 'axios'; // 引入 axios
import { getToken } from "@/utils/auth";

const { proxy } = getCurrentInstance();

const deviceList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const baseUrl = import.meta.env.VITE_APP_BASE_API;
// const headers = ref({ Authorization: "Bearer " + getToken() });

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    deviceName: null,
  },
  rules: {
    deviceName: [
      { required: true, message: "仪器名称不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询仪器管理列表 */
function getList() {
  loading.value = true;
  listDevice(queryParams.value).then(response => {
    deviceList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 表单重置 */
function reset() {
  form.value = {
    deviceId: null,
    deviceName: null,
    deviceImg: null,
    createBy: null,
    createTime: null,
    updateBy: null,
    updateTime: null,
  };
  proxy.resetForm("deviceRef");
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
  ids.value = selection.map(item => item.deviceId);
  single.value = selection.length != 1;
  multiple.value = !selection.length;
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('resource/device/export', {
    ...queryParams.value
  }, `device_${new Date().getTime()}.xlsx`);
}

getList();
</script>