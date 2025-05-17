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
        <el-button type="primary" plain icon="Plus" @click="handleAdd"
          v-hasPermi="['resource:device:add']">新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="success" plain icon="Edit" :disabled="single" @click="handleUpdate"
          v-hasPermi="['resource:device:edit']">修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="danger" plain icon="Delete" :disabled="multiple" @click="handleDelete"
          v-hasPermi="['resource:device:remove']">删除</el-button>
      </el-col>
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
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)"
            v-hasPermi="['resource:device:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)"
            v-hasPermi="['resource:device:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum"
      v-model:limit="queryParams.pageSize" @pagination="getList" />

    <!-- 添加或修改仪器管理对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="deviceRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item v-if="renderField(true, true)" label="仪器名称" prop="deviceName">
          <el-input v-model="form.deviceName" placeholder="请输入仪器名称" />
        </el-form-item>
        <el-form-item v-if="renderField(true, true)" label="仪器图片" prop="deviceImg">
          <image-upload v-model="form.deviceImg" limit="1" />
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

/** 取消按钮 */
function cancel() {
  open.value = false;
  // 处理图片删除
  if (form.value.deviceImg) {
    const fileName = form.value.deviceImg.replace(baseUrl, '').replace('/profile/', '');
    axios.delete(`${baseUrl}/common/delete`, {
      params: { fileName },
      headers: {
        Authorization: "Bearer " + getToken()
      }
    });
  }
  reset();
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

/** 新增按钮操作 */
function handleAdd() {
  reset();
  open.value = true;
  title.value = "添加仪器管理";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _deviceId = row.deviceId || ids.value;
  getDevice(_deviceId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改仪器管理";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["deviceRef"].validate(valid => {
    if (valid) {
      if (form.value.deviceId != null) {
        updateDevice(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addDevice(form.value).then(response => {
          proxy.$modal.msgSuccess("新增成功");
          open.value = false;
          getList();
        });
      }
    }
  });
}

/** 删除按钮操作 */
// function handleDelete(row) {
//   const _deviceIds = row.deviceId || ids.value;
//   proxy.$modal.confirm('是否确认删除仪器管理编号为"' + _deviceIds + '"的数据项？').then(function () {

//     return delDevice(_deviceIds);
//   }).then(() => {
//     getList();
//     proxy.$modal.msgSuccess("删除成功");
//   }).catch(() => { });
// }

async function handleDelete(row) {
  const deviceIds = row.deviceId || ids.value;

  try {
    // 确认删除
    await proxy.$modal.confirm(`是否确认删除仪器管理编号为"${deviceIds}"的数据项？`);

    // 处理图片删除
    if (!Array.isArray(deviceIds)) {
      if (row.deviceImg) {
        const fileName = row.deviceImg.replace(baseUrl, '').replace('/profile/', '');
        await axios.delete(`${baseUrl}/common/delete`, {
          params: { fileName },
          headers: {
            Authorization: "Bearer " + getToken()
          }
        });
      }
    } else {
      const deviceImg = deviceList.value.filter(item => Array.isArray(ids.value)
        && ids.value.includes(item.deviceId)).map(item => item.deviceImg)
      for (let i = deviceImg.length - 1; i >= 0; i--) {
        const currentItem = deviceImg[i];
        if (currentItem) {
          const fileName = currentItem.replace(baseUrl, '').replace('/profile/', '');
          await axios.delete(`${baseUrl}/common/delete`, {
            params: { fileName },
            headers: {
              Authorization: "Bearer " + getToken()
            }
          });
        }
      }
    }
    // 处理设备删除
    await delDevice(deviceIds);

    // 更新列表并显示成功消息
    getList();
    proxy.$modal.msgSuccess("删除成功");
  } catch (error) {
    // 错误处理
    console.error("删除失败:", error);
    proxy.$modal.msgError("删除失败，请重试");
  }
}



/** 导出按钮操作 */
function handleExport() {
  proxy.download('resource/device/export', {
    ...queryParams.value
  }, `device_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.deviceId == null ? insert : edit;
}

getList();
</script>