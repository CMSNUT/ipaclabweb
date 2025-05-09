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