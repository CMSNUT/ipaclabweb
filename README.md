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
# 增加模块1: 仪器管理
```bash
-- ----------------------------
-- 1、仪器信息表
-- ----------------------------
create table sys_instrument (
  instrument_id           int(4)      not null auto_increment    comment '仪器ID',
  instrument_name         varchar(30)     not null                   comment '仪器名称',
  instrument_model        varchar(30)     default ''                 comment '仪器型号',
  instrument_remark       varchar(200)    default null               comment '功能简介',
  instrument_room         varchar(20)      default null               comment '存放位置',
  instrument_img          varchar(200)    default ''                 comment '图片地址',
  create_by         varchar(64)     default ''                 comment '创建者',
  create_time       datetime                                   comment '创建时间',
  update_by         varchar(64)     default ''                 comment '更新者',
  update_time       datetime                                   comment '更新时间',
  primary key (instrument_id)
) engine=innodb auto_increment=100 comment = '仪器信息表';
```

```bash
-- ----------------------------
-- 2、仪器教程表
-- ----------------------------
create table sys_instrument_tutorial (
  tutorial_id           int(4)      not null auto_increment    comment '教程ID',
  instrument_id         int(4)      default null    comment '仪器ID',
  tutorial_title         varchar(30)     not null                   comment '教程标题',
  tutorial_category      char(1)       default '0'                 comment '教程类别(0文本 1视频)',
  tutorial_file       varchar(200)    default null                  comment '本地文件',
  tutorial_url        varchar(200)    default null                  comment '外部链接',
  create_by         varchar(64)     default ''                 comment '创建者',
  create_time       datetime                                   comment '创建时间',
  update_by         varchar(64)     default ''                 comment '更新者',
  update_time       datetime                                   comment '更新时间',
  primary key (tutorial_id)
) engine=innodb auto_increment=100 comment = '仪器教程表';
```
## 仪器教程的前端操作修改
- 参考 system/user/index.vue
```bash

```

```bash
```

