<template>
    <div class="app-container">
      <el-card shadow="never">
        <template #header>
          <div class="clearfix">
            <span>仪器详情</span>
            <el-button style="float: right; padding: 3px 0" type="link" @click="goBack">
              返回列表
            </el-button>
          </div>
        </template>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form label-width="120px">
              <el-form-item label="仪器ID">
                <span>{{ device.deviceId }}</span>
              </el-form-item>
              <el-form-item label="仪器名称">
                <span>{{ device.deviceName }}</span>
              </el-form-item>
              <el-form-item label="仪器型号">
                <span>{{ device.deviceModel }}</span>
              </el-form-item>
              <el-form-item label="功能简介">
                <span>{{ device.deviceRemark }}</span>
              </el-form-item>
              <el-form-item label="存放位置">
                <span>{{ device.deviceRoom }}</span>
              </el-form-item>
            </el-form>
          </el-col>
          <!-- <el-col :span="12">
            <el-image
              v-if="device.deviceImg"
              :src="device.deviceImg"
              :fit="cover"
              style="width: 200px; height: 200px"
            >
              <template #error>
                <img src="@/assets/images/default.png" alt="默认图片" style="width: 200px; height: 200px" />
              </template>
            </el-image>
          </el-col> -->
        </el-row>
      </el-card>
      
      <!-- 仪器教程列表 -->
      <el-card class="mt-4" shadow="never">
        <template #header>
          <div class="flex justify-between items-center">
            <span>仪器教程</span>
            <el-button 
              v-if="device.deviceId" 
              type="primary" 
              size="small" 
              @click="addNewTutorial"
            >
              <i class="fa fa-plus mr-1"></i>添加教程
            </el-button>
          </div>
        </template>
        
        <div v-if="loadingTutorialList" class="py-10 text-center">
          <el-loading-spinner size="large"></el-loading-spinner>
          <p class="mt-2 text-gray-500">加载教程中...</p>
        </div>
        
        <el-empty v-else-if="!tutorialList.length" description="暂无教程"></el-empty>
        
        <el-table 
          v-else
          :data="tutorialList" 
          stripe 
          border
          @row-click="handleTutorialClick"
        >
          <el-table-column prop="tutorialTitle" label="教程标题" min-width="200" :show-overflow-tooltip="true"></el-table-column>
          <el-table-column prop="tutorialFile" label="教程文档" min-width="200" :show-overflow-tooltip="true"> 
          </el-table-column>

          <el-table-column prop="tutorialUrl" label="教程链接" width="120" :show-overflow-tooltip="true"> 
            <template #default="scope">
              <a :href="scope.row.tutorialUrl" target="_blank" class="text-primary hover:underline">
                <dict-tag :options="sys_tutorial_category" :value="scope.row.tutorialCategory"/>
              </a>
            </template>
          </el-table-column>

          <el-table-column prop="createBy" label="创建者" width="120" :show-overflow-tooltip="true"></el-table-column>
          <el-table-column prop="createTime" label="创建时间" width="160" :show-overflow-tooltip="true"></el-table-column>
          <el-table-column prop="updateBy" label="更新者" width="120" :show-overflow-tooltip="true"></el-table-column>
          <el-table-column prop="updateTime" label="创建时间" width="160" :show-overflow-tooltip="true"></el-table-column>
        </el-table>
      </el-card>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, watch } from 'vue'
  import { useRoute, useRouter } from 'vue-router'
  import { getDevice } from '@/api/system/device'
  import { ElMessage, ElMessageBox } from 'element-plus'

  import { listDevice_tutorial } from "@/api/system/device_tutorial";

  const { proxy } = getCurrentInstance();
  const { sys_tutorial_category } = proxy.useDict('sys_tutorial_category');

  const tutorialList = ref([]); 
  const route = useRoute()
  const router = useRouter()
  const device = ref({})
  const tutorials = ref([])
  const loading = ref(true)
  const loadingTutorialList = ref(true)
  
  // 获取仪器详情
  const fetchDeviceDetail = async () => {
    try {
      const deviceId = route.params.deviceId
      if (!deviceId) {
        ElMessage.error('缺少设备ID参数')
        router.go(-1)
        return
      }
      
      const response = await getDevice(deviceId)
      device.value = response.data || {}
    } catch (error) {
      console.error('获取仪器详情失败', error)
      ElMessage.error('获取仪器详情失败，请稍后重试')
    } finally {
      loading.value = false
    }
  }
  
  // 获取仪器教程列表
  // const fetchTutorials = async () => {
  //   try {
  //     const deviceId = route.params.deviceId
  //     if (!deviceId) return
      
  //     loadingTutorials.value = true
  //     const response = await getTutorialsByDeviceId(deviceId)
  //     tutorials.value = response.data || []
  //   } catch (error) {
  //     console.error('获取教程列表失败', error)
  //     ElMessage.error('获取教程列表失败，请稍后重试')
  //   } finally {
  //     loadingTutorials.value = false
  //   }
  // }

  const data = reactive({
    queryParams: {
      deviceId: null,
    },
  });
  const { queryParams } = toRefs(data);

  function fetchTutorials() {
    loadingTutorialList.value = true;
    queryParams.value.deviceId = route.params.deviceId
    listDevice_tutorial(queryParams.value).then(response => {
      tutorialList.value = response.rows;
      console.log("tutorialList.value:", tutorialList.value)
      // total.value = response.total;
      loadingTutorialList.value = false;
    });
  }
  
  // 返回列表页
  const goBack = () => {
    router.go(-1)
  }
  
  // 添加新教程
  const addNewTutorial = () => {
    const deviceId = route.query.deviceId
    if (deviceId) {
      router.push({
        name: 'AddTutorial',
        query: { deviceId }
      })
    }
  }
  
  // 查看教程
  const viewTutorial = (tutorial) => {
    router.push({
      name: 'ViewTutorial',
      params: { id: tutorial.id }
    })
  }
  
  // 编辑教程
  const editTutorial = (tutorial) => {
    router.push({
      name: 'EditTutorial',
      params: { id: tutorial.id }
    })
  }
  
  // 删除教程
  const deleteTutorial = async (tutorial) => {
    try {
      await ElMessageBox.confirm(
        `确定要删除教程 "${tutorial.title}" 吗？`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
      
      // 调用删除API
      // await deleteTutorialApi(tutorial.id)
      
      // 从列表中移除
      tutorials.value = tutorials.value.filter(item => item.id !== tutorial.id)
      ElMessage.success('教程删除成功')
    } catch (error) {
      // 用户取消操作
    }
  }
  
  // 监听设备ID变化，重新加载数据
  // watch(
  //   () => route.params.deviceId,
  //   (newVal) => {
  //     if (newVal) {
  //       fetchDeviceDetail()
  //       fetchTutorials()
  //     }
  //   },
  //   { immediate: true }
  // )
  
  onMounted(() => {
    fetchDeviceDetail()
    fetchTutorials()
  })
  </script>
  
  <style scoped>
  .mt-4 {
    margin-top: 1rem;
  }
  
  .flex {
    display: flex;
  }
  
  .justify-between {
    justify-content: space-between;
  }
  
  .items-center {
    align-items: center;
  }
  </style>