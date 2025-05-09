<template>
  <div class="app-container">
    <!-- 搜索表单 -->
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <!-- <el-form-item label="仪器ID" prop="deviceId">
        <el-select v-model="queryParams.deviceId" placeholder="请选择仪器ID" clearable style="width: 240px">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item> -->
      <el-form-item label="仪器名称" prop="deviceId">
        <el-select v-model="queryParams.deviceId" placeholder="请选择仪器" clearable style="width: 240px">
          <el-option
            v-for="item in deviceList"
            :key="item.value"
            :label="item.label"
            :value="item.value"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="教程标题" prop="tutorialTitle">
        <el-input
          v-model="queryParams.tutorialTitle"
          placeholder="请输入教程标题"
          clearable
          style="width: 240px"
          @keyup.enter="handleQuery"
        />
      </el-form-item>
      <el-form-item label="教程类别" prop="tutorialCategory">
        <el-select v-model="queryParams.tutorialCategory" placeholder="请选择教程类别" clearable style="width: 240px">
          <el-option
            v-for="dict in sys_tutorial_category"
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

    <!-- 按钮区域 -->
    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button
          type="primary"
          plain
          icon="Plus"
          @click="handleAdd"
          v-hasPermi="['system:device_tutorial:add']"
        >新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="success"
          plain
          icon="Edit"
          :disabled="single"
          @click="handleUpdate"
          v-hasPermi="['system:device_tutorial:edit']"
        >修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="danger"
          plain
          icon="Delete"
          :disabled="multiple"
          @click="handleDelete"
          v-hasPermi="['system:device_tutorial:remove']"
        >删除</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button
          type="warning"
          plain
          icon="Download"
          @click="handleExport"
          v-hasPermi="['system:device_tutorial:export']"
        >导出</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <!-- 显示表格 -->
    <el-table v-loading="loading" :data="device_tutorialList" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="教程ID" align="center" prop="tutorialId" />
      <!-- <el-table-column label="仪器ID" align="center" prop="deviceId" /> -->
      
      <!-- 修改：添加自定义函数显示仪器名称 -->
      
      <el-table-column label="仪器名称" align="center" prop="deviceId">
        <template #default="scope">
          <!-- <dict-tag :options="deviceList" :value="scope.row.deviceId" /> -->
          {{ getDeviceName(scope.row.deviceId) }}
        </template>
      </el-table-column>

      <el-table-column label="教程标题" align="center" prop="tutorialTitle" :show-overflow-tooltip="true" />
      <el-table-column label="教程类别" align="center" prop="tutorialCategory">
        <template #default="scope">
            <dict-tag :options="sys_tutorial_category" :value="scope.row.tutorialCategory"/>
        </template>
      </el-table-column>
      <el-table-column label="操作" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['system:device_tutorial:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['system:device_tutorial:remove']">删除</el-button>
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

    <!-- 添加或修改仪器教程对话框 -->
    <el-dialog :title="title" v-model="open" width="500px" append-to-body>
      <el-form ref="device_tutorialRef" :model="form" :rules="rules" label-width="80px">
      <!-- <el-form-item v-if="renderField(true, true)" label="仪器ID" prop="deviceId">
        <el-select v-model="form.deviceId" placeholder="请选择仪器ID">
          <el-option label="请选择字典生成" value="" />
        </el-select>
      </el-form-item> -->
      <el-form-item v-if="renderField(true, true)" label="仪器名称" prop="deviceId">
          <el-select v-model="form.deviceId" placeholder="请选择仪器">
            <el-option
              v-for="item in deviceList"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="教程标题" prop="tutorialTitle">
        <el-input v-model="form.tutorialTitle" placeholder="请输入教程标题" />
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="教程类别" prop="tutorialCategory">
        <el-select v-model="form.tutorialCategory" placeholder="请选择教程类别">
          <el-option
            v-for="dict in sys_tutorial_category"
            :key="dict.value"
            :label="dict.label"
            :value="dict.value"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="本地文件" prop="tutorialFile">
        <file-upload v-model="form.tutorialFile"/>
      </el-form-item>
      <el-form-item v-if="renderField(true, true)" label="外部链接" prop="tutorialUrl">
        <el-input v-model="form.tutorialUrl" placeholder="请输入外部链接" />
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

<script setup name="Device_tutorial">
import { listDevice_tutorial, getDevice_tutorial, delDevice_tutorial, addDevice_tutorial, updateDevice_tutorial } from "@/api/system/device_tutorial";
import { listDevice } from "@/api/system/device"; // 新增：导入仪器API


const { proxy } = getCurrentInstance();
const { sys_tutorial_category } = proxy.useDict('sys_tutorial_category');

const device_tutorialList = ref([]);
const open = ref(false);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);
const title = ref("");
const deviceList = ref([]); // 新增：仪器字典状态

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    deviceId: null,
    tutorialTitle: null,
    tutorialCategory: null,
  },
  rules: {
    tutorialTitle: [
      { required: true, message: "教程标题不能为空", trigger: "blur" }
    ],
  }
});

const { queryParams, form, rules } = toRefs(data);

/** 查询仪器教程列表 */
function getList() {
  loading.value = true;
  listDevice_tutorial(queryParams.value).then(response => {
    device_tutorialList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
}

/** 新增: 根据设备ID获取设备名称 */
const getDeviceName = (deviceId) => {
  if (!deviceId || deviceList.value.length === 0) return '-';
  const device = deviceList.value.find(item => item.value === deviceId);
  return device ? device.label : `未知仪器(${deviceId})`;
};

// 新增：加载仪器列表
const getDeviceList = () => {
  listDevice().then(response => {
  deviceList.value = response.rows.map(item => ({
    label: item.deviceName,
    value: item.deviceId    
  }));
})
};

/** 取消按钮 */
function cancel() {
  open.value = false;
  reset();
}

/** 表单重置 */
function reset() {
  form.value = {
    tutorialId: null,
    deviceId: null,
    tutorialTitle: null,
    tutorialCategory: null,
    tutorialFile: null,
    tutorialUrl: null,
    createBy: null,
    createTime: null,
    updateBy: null,
    updateTime: null,
  };
  proxy.resetForm("device_tutorialRef");
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
  title.value = "添加仪器教程";
}

/** 修改按钮操作 */
function handleUpdate(row) {
  reset();
  const _tutorialId = row.tutorialId || ids.value;
  getDevice_tutorial(_tutorialId).then(response => {
    form.value = response.data;
    open.value = true;
    title.value = "修改仪器教程";
  });
}

/** 提交按钮 */
function submitForm() {
  proxy.$refs["device_tutorialRef"].validate(valid => {
    if (valid) {
      if (form.value.tutorialId != null) {
        updateDevice_tutorial(form.value).then(response => {
          proxy.$modal.msgSuccess("修改成功");
          open.value = false;
          getList();
        });
      } else {
        addDevice_tutorial(form.value).then(response => {
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
  proxy.$modal.confirm('是否确认删除仪器教程编号为"' + _tutorialIds + '"的数据项？').then(function() {
    return delDevice_tutorial(_tutorialIds);
  }).then(() => {
    getList();
    proxy.$modal.msgSuccess("删除成功");
  }).catch(() => {});
}


/** 导出按钮操作 */
function handleExport() {
  proxy.download('system/device_tutorial/export', {
    ...queryParams.value
  }, `device_tutorial_${new Date().getTime()}.xlsx`);
}

/** 是否渲染字段 */
function renderField(insert, edit) {
  return form.value.tutorialId == null ? insert : edit;
}

getDeviceList(); // 新增
getList();
</script>