<!-- <template>
  <div class="app-container">
    {{route.params.deviceId}}

    仪器设备{{ route.params.deviceId }}详情页面
  </div>
</template> -->

<template>
  <div class="app-container">
    <el-card shadow="never">
      <template #header>
        <div class="clearfix">
          <span>仪器详情</span>
          <el-button style="float: right; padding: 3px 0" type="text" @click="goBack">
            返回列表
          </el-button>
        </div>
      </template>
      
      <!-- 显示仪器详情内容 -->
      <div v-if="device" class="device-detail">
        <div class="detail-row">
          <span class="detail-label">仪器ID:</span>
          <span class="detail-value">{{ device.deviceId }}</span>
        </div>
        <div class="detail-row">
          <span class="detail-label">仪器名称:</span>
          <span class="detail-value">{{ device.deviceName }}</span>
        </div>
        <!-- 其他字段... -->
      </div>
      
      <!-- 加载状态 -->
      <div v-else class="loading">
        <el-loading-spinner></el-loading-spinner>
        <p>加载中...</p>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { getDevice } from '@/api/system/device';

const route = useRoute();
const router = useRouter();
const device = ref(null);
const loading = ref(true);

// 获取仪器详情
const fetchDeviceDetail = async () => {
  try {
    const deviceId = route.params.deviceId;
    const response = await getDevice(deviceId);
    device.value = response.data;
  } catch (error) {
    console.error('获取仪器详情失败', error);
    // 显示错误提示
  } finally {
    loading.value = false;
  }
};

// 返回列表
const goBack = () => {
  router.go(-1);
};

onMounted(() => {
  fetchDeviceDetail();
});
</script>