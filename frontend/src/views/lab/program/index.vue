<template>
  <div class="app-container">
    <!-- 搜索表单 -->
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch" label-width="68px">
      <!-- 程序名称输入框 -->
      <el-form-item label="程序名称" prop="algoName">
        <el-input v-model="queryParams.algoName" placeholder="请输入程序名称" clearable style="width: 240px"
          @keyup.enter="handleQuery" />
      </el-form-item>
      <!-- 程序类型选择框 -->
      <el-form-item label="程序类型" prop="algoType">
        <el-select v-model="queryParams.algoType" placeholder="请选择程序类型" clearable style="width: 240px">
          <el-option v-for="dict in sys_program_type" :key="dict.value" :label="dict.label" :value="dict.value" />
        </el-select>
      </el-form-item>
      <!-- 编程语言选择框 -->
      <el-form-item label="编程语言" prop="algoLang">
        <el-select v-model="queryParams.algoLang" placeholder="请选择编程语言" clearable style="width: 240px">
          <el-option v-for="dict in sys_program_lang" :key="dict.value" :label="dict.label" :value="dict.value" />
        </el-select>
      </el-form-item>
      <!-- 搜索和重置按钮 -->
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
      
    </el-form>
    <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>

    <!-- 卡片模式 -->
    <el-row :gutter="20" v-loading="loading">
      <el-col 
        v-for="item in algoList"
        :key="item.algoId"
        :xs="24" :sm="12" :md="8" :lg="6" :xl="4"
      >
        <el-card class="box-card">
          <div class="content">
            <!-- 使用v-html渲染富文本 -->
            <div 
              class="rich-content" 
              v-html="sanitizeHtml(item.algoDesc)"
            ></div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 分页组件 -->
    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum" v-model:limit="queryParams.pageSize"
      @pagination="getList" />
  </div>
</template>

<script setup name="Algo">
import { listAlgo } from "@/api/resource/algo";
import { ref, getCurrentInstance, } from 'vue';
// 在原有导入基础上增加时间格式化方法
// import { parseTime } from '@/utils/ruoyi'
import DOMPurify from 'dompurify' // 安全过滤库

// 安全过滤方法
const sanitizeHtml = (html) => {
  return DOMPurify.sanitize(html || '<i>暂无内容</i>', {
    ALLOWED_TAGS: ['p', 'b', 'i', 'u', 'strong', 'em', 'br', 'img', 'h1', 'h2', 'h3', 'ul', 'ol', 'li'],
    ALLOWED_ATTR: ['style', 'src', 'alt', 'class']
  })
}

const { proxy } = getCurrentInstance();
const { sys_program_type, sys_program_lang } = proxy.useDict('sys_program_type', 'sys_program_lang');

const algoList = ref([]);
const loading = ref(true);
const showSearch = ref(true);
const ids = ref([]);
const single = ref(true);
const multiple = ref(true);
const total = ref(0);

const data = reactive({
  form: {},
  queryParams: {
    pageNum: 1,
    pageSize: 10,
    algoName: null,
    algoDesc: null,
    algoType: null,
    algoLang: null,
    orderByColumn: 'create_time', // 新增排序字段
    isAsc: 'desc' // 降序排列
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

const { queryParams } = toRefs(data);

/** 查询程序管理列表 */
function getList() {
  loading.value = true;
  listAlgo(queryParams.value).then(response => {
    algoList.value = response.rows;
    total.value = response.total;
    loading.value = false;
  });
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


getList();
</script>

<style scoped>
/* 卡片容器 */
.card-col {
  margin-bottom: 20px;
}

/* 卡片主体样式 */
.box-card {
  height: 200px;
  display: flex;
  flex-direction: column;
  transition: box-shadow 0.3s;
}

/* 卡片内容布局 */
.box-card .el-card__body {
  flex: 1;
  padding: 15px;
  display: flex;
  flex-direction: column;
}

/* 卡片头部样式 */
.card-header {
  border-bottom: 1px solid #eeeeee;
  padding-bottom: 10px;
  margin-bottom: 10px;
}

.card-header .title {
  font-size: 16px;
  font-weight: 600;
  color: #333333;
  margin-right: 8px;
}

/* 标签容器 */
.meta {
  margin-top: 8px;
  display: flex;
  gap: 5px;
}

/* 内容区域 */
.content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

/* 多行文本截断方案 */
.description {
  color: #666666;
  font-size: 13px;
  line-height: 1.5;
  
  /* 现代浏览器方案 */
  display: -webkit-box;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  -webkit-line-clamp: 3;
  
  /* 标准属性（未来兼容） */
  line-clamp: 3;
  
  /* 旧版Firefox备用方案 */
  max-height: 4.5em; /* 3行 x 1.5行高 */
  position: relative;
}

/* Firefox备用省略号 */
@supports (overflow: -moz-hidden-unscrollable) {
  .description {
    display: block;
  }
  .description::after {
    content: "...";
    position: absolute;
    right: 0;
    bottom: 0;
    background: linear-gradient(to right, transparent, white 50%);
    padding-left: 5px;
  }
}

/* 底部信息 */
.footer {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #999999;
}

.footer .time {
  display: flex;
  align-items: center;
  gap: 3px;
}

/* 响应式布局 */
@media (max-width: 768px) {
  .card-col {
    width: 100%;
  }
}

@media (min-width: 769px) and (max-width: 992px) {
  .card-col {
    width: 50%;
  }
}

@media (min-width: 993px) and (max-width: 1200px) {
  .card-col {
    width: 33.33%;
  }
}

@media (min-width: 1201px) {
  .card-col {
    width: 25%;
  }
}

/* 卡片hover效果 */
.box-card:hover {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}


.rich-content {
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

.rich-content p {
  margin: 0.8em 0;
  color: #333;
}

.rich-content img {
  max-width: 100%;
  height: auto;
  margin: 10px 0;
  border-radius: 4px;
}

.rich-content h1, 
.rich-content h2, 
.rich-content h3 {
  margin: 1.2em 0 0.8em;
  color: #222;
}

.rich-content ul, 
.rich-content ol {
  padding-left: 2em;
  margin: 0.8em 0;
}

.rich-content li {
  margin: 0.4em 0;
}

.rich-content table {
  width: 100%;
  margin: 1em 0;
  border-collapse: collapse;
}

.rich-content td, 
.rich-content th {
  padding: 8px;
  border: 1px solid #ddd;
}

.rich-content pre {
  background: #f6f8fa;
  padding: 1em;
  border-radius: 4px;
  overflow-x: auto;
}

.rich-content code {
  font-family: Monaco, Consolas, "Courier New", monospace;
  background: #f3f3f3;
  padding: 2px 4px;
  border-radius: 3px;
}
</style>