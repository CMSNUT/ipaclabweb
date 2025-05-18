# 项目初始化
## 前端
### 安装依赖
```bash
cd frontend
npm i
```
### 运行app
- **修改后端API端口**
```bash
// vite 相关配置
    server: {
      port: 3000,  # 开发环境前端 端口改为 3000
      host: true,
      open: true,
      proxy: {
        // https://cn.vitejs.dev/config/#server-proxy
        '/dev-api': {
          target: 'http://127.0.0.1:8000',  # 后端端口改为 8000
          changeOrigin: true,
          rewrite: (p) => p.replace(/^\/dev-api/, '')
        }
      }
    }，
```

## 后端
### 修改环境配置
- mysql 的配置进行修改

### 安装依赖
- Anaconda 创建虚拟环境 ipac-env
- 安装依赖
```bash
conda create -n ipac-env python=3.9 -y
conda activate ipac-env
pip install -r xxx\\requirements.txt
```

## 安装wangEditor
```bash
npm install @wangeditor/editor @wangeditor/editor-for-vue@next --save
```

# 增加模块
## 生成代码
- 在前端 `代码生成` 菜单项，点击`创建`，然后将建表代码复制到对话框中
```bash
-- ----------------------------
-- 1、仪器信息表
-- ----------------------------
create table sys_device (
  device_id           int(4)      not null auto_increment    comment '仪器ID',
  device_name         varchar(30)     not null                   comment '仪器名称',
  device_model        varchar(30)     default ''                 comment '仪器型号',
  device_remark       varchar(200)    default null               comment '功能简介',
  device_room         varchar(20)      default null               comment '存放位置',
  device_img          varchar(200)    default ''                 comment '图片地址',
  create_by         varchar(30)     default ''                 comment '创建者',
  create_time       datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新者',
  update_time       datetime                                   comment '更新时间',
  primary key (device_id)
) engine=innodb auto_increment=1 comment = '仪器信息表';
```

```bash
-- ----------------------------
-- 2、仪器教程表
-- ----------------------------
create table sys_device_tutorial (
  tutorial_id           int(4)      not null auto_increment    comment '教程ID',
  device_id         int(4)      default null    comment '仪器ID',
  tutorial_title         varchar(30)     not null                   comment '教程标题',
  tutorial_category      char(1)       default '0'                 comment '教程类别(0文本 1视频)',
  tutorial_file       varchar(200)    default null                  comment '本地文件',
  tutorial_url        varchar(200)    default null                  comment '外部链接',
  create_by         varchar(30)     default ''                 comment '创建者',
  create_time       datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新者',
  update_time       datetime                                   comment '更新时间',
  primary key (tutorial_id)
) engine=innodb auto_increment=1 comment = '仪器教程表';
```
## 代码修改和完善
- 点击 `修改`，修改`字段信息` 和 `生成信息`

## 代码应用
- 点击`生成`，下载代码
- 解压后，复制 `backend` 文件夹 到 项目根目录
- 复制 `frontend` 文件夹中的 `api` 和 `views` 文件夹，到项目的`frontend\src`文件夹中
- 在 项目`backend\server.py` 文件中，添加 新增模块的 控制器
- 使用mysql命令，添加新增模块的菜单信息

# 关键点备忘
## 代码生成
[X] 使用`代码生成`数据表时，字典需要先生成，且字段显示设为下拉菜单
[X] 选择框，显示都可以设为下拉菜单
[X] 图片地址，显示设为`图片上传`
[X] 文件地址，显示设为`文件上传`
[X] 富文本，字段类型设为 text，显示设为 `富文本`

## 前端代码
### 外键ID 显示为名称
- `script`部分
```JavaScript
import { listDevice } from "@/api/system/device"; // 新增：导入仪器API

const deviceList = ref([]); // 新增：仪器字典状态


/** 新增: 自定义函数，根据设备ID获取设备名称 */
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

getDeviceList(); // 新增
```
- 搜索部分
```vue
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
```
- 表格部分
```vue
<!-- 修改：添加自定义函数显示仪器名称 -->
      
<el-table-column label="仪器名称" align="center" prop="deviceId">
  <template #default="scope">
    {{ getDeviceName(scope.row.deviceId) }}
  </template>
</el-table-column>
```
- 修改或新增对话框部分
```vue
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
```

# 路由设置
- 以`仪器设备`及`仪器详情`为例
## `query` 模式
- `resource/instrument/index.vue`
```vue
<!-- - `resource/instrument/index.vue` -->
<el-table-column label="仪器名称" align="center" :show-overflow-tooltip="true">
  <template #default="scope">
    <router-link :to="{ name: 'InstrumentDetail', query: {id: scope.row.deviceId }}" class="link-type">
      <span>{{ scope.row.deviceName }}</span>
    </router-link>
  </template>
</el-table-column>
```
- `resource/instrument/detail.vue`
```JavaScript
// `resource/instrument/detail.vue` 
......
const deviceId = route.query.id;
......
```

- `router/index.js`
```JavaScript
// 动态路由，基于用户权限动态去加载
......
{
  path: '/resource',
  component: Layout,
  hidden: true,
  // roles: ['admin','common'],
  permissions: ['system:device:list','system:device:query'],
  children: [
    {
      path: '/resource/instrument/detail', // 注意这里不需要动态参数
      component: () => import('@/views/resource/instrument/detail'),
      name: 'InstrumentDetail',
      roles: ['admin','common'],
      permissions: ['system:device:list','system:device:query'],
      meta: { title: '仪器详情' }
    }
  ]
}

......
```

## `params`模式
- `resource/instrument/index.vue`
```vue
<!-- - `resource/instrument/index.vue` -->
<el-table-column label="仪器名称" align="center" :show-overflow-tooltip="true">
  <template #default="scope">
    <router-link :to="'/resource/instrument/' + scope.row.deviceId" class="link-type">   
      <span>{{ scope.row.deviceName }}</span>
    </router-link>
  </template>
</el-table-column>
```

- `resource/instrument/detail.vue`
```JavaScript
// `resource/instrument/detail.vue` 
......
const deviceId = route.params.deviceId;
......
```
- `router/index.js`
```JavaScript
// 动态路由，基于用户权限动态去加载
{
  path: '/resource',
  component: Layout,
  hidden: true,
  roles: ['admin','common'],
  permissions: ['system:device:list','system:device:query'],
  children: [
    {
      path: 'instrument/:deviceId(\\d+)',
      component: () => import('@/views/resource/instrument/detail'),
      name: 'InstrumentDetail',
      meta: { title: '仪器设备详情', activeMenu: '/resource/instrument' }
    }
  ]
}
```

## 系统管理中菜单设置(`params`模式)
|菜单名称|路由名称|路由地址|组件路径|权限字符|菜单显示|
|----|----|----|----|----|----|
|仪器设备|`Instrument`|`instrument`|`resource/instrument/index`|`system:device:list`|显示|
|仪器详情|`InstrumentDetail`|`instrument`|`resource/instrument/detail`|`system:device:query`|不显示|
|仪器教程|InstrumentTutorial||||不显示|
|仪器教程详情|InstrumentTutorialDetail||||不显示|

## 系统管理中权限设置
- 授权非管理员`学习资源`下所有菜单的权限


# 其他表设计

## 标签表
```bash
-- ----------------------------
-- 1、标签表
-- ----------------------------


```

## 算法程序表
```bash
-- ----------------------------
-- 1、算法程序表
-- ----------------------------
create table sys_algo (
  algo_id           int(8)      not null auto_increment    comment '算法ID',
  algo_name        varchar(30)  not null                   comment '算法名称',
  algo_lang         char(1)         default '0'            comment '编程语言',
  algo_desc         mediumtext   default null                   comment '算法描述',
  create_by         varchar(30)   default ''                 comment '创建者',
  create_time       datetime                                   comment '创建时间',
  update_by         varchar(30)   default ''                 comment '更新者',
  update_time       datetime                                   comment '更新时间',
  primary key (algo_id)
) engine=innodb auto_increment=1 comment = '算法程序表';
```

```bash
-- ----------------------------
-- 2、算法教程表
-- ----------------------------
create table sys_algo_tutorial (
  tutorial_id           int(4)      not null auto_increment    comment '教程ID',
  algo_id         int(4)      default null    comment '算法ID',
  tutorial_title         varchar(30)     not null   comment '教程标题',
  tutorial_content       mediumtext   default null   comment '教程内容(富文本)',
  create_by         varchar(30)     default ''                 comment '创建者',
  create_time       datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新者',
  update_time       datetime                                   comment '更新时间',
  primary key (tutorial_id)
) engine=innodb auto_increment=1 comment = '算法教程表';
```



## 待完善
- **移动端界面美化**
- **原位查看文件**

