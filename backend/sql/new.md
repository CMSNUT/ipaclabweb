# 仪器设备
## 设备列表
```bash
-- ----------------------------
-- 1、仪器表
-- ----------------------------
create table sys_device (
  device_id         int(3)        not null auto_increment      comment '仪器id',
  device_name       varchar(50)   not null                     comment '仪器名称',
  device_img        varchar(100)  default null                 comment '仪器图片地址',
  device_desc       varchar(512)  default null                 comment '仪器简介',
  create_by         varchar(30)     default ''                 comment '创建人',
  create_time 	    datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新人',
  update_time       datetime                                   comment '更新时间',
  primary key (device_id)
) engine=innodb auto_increment=1 comment = '仪器表';
```

## 设备教程
```bash
-- ----------------------------
-- 2、仪器教程表
-- ----------------------------
create table sys_device_tutorial (
  tutorial_id        int(6)        not null auto_increment      comment '教程id',
  tutorial_name     varchar(80)   not null                     comment '教程名称',
  device_id         int(3)          not null                   comment '仪器id',
  tutorial_content  mediumtext      default null               comment '教程内容',
  create_by         varchar(30)     default ''                 comment '创建人',
  create_time 	    datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新人',
  update_time       datetime                                   comment '更新时间',
  primary key (tutorial_id)
) engine=innodb auto_increment=1 comment = '仪器教程表';
```

# 算法程序
## 程序列表
```bash
-- ----------------------------
-- 3、算法表
-- ----------------------------
create table sys_algo (
  algo_id         int(6)        not null auto_increment      comment '算法id',
  algo_name       varchar(80)   not null                     comment '算法名称',
  algo_type       char(1)       default '0'                  comment '算法类别',
  algo_lang       char(1)       default '0'                  comment '算法语言',
  algo_content    mediumtext    default null                 comment '算法详情',
  create_by         varchar(30)     default ''                 comment '创建人',
  create_time 	    datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新人',
  update_time       datetime                                   comment '更新时间',
  primary key (algo_id)
) engine=innodb auto_increment=1 comment = '算法表';
```
## 算法教程
```bash
-- ----------------------------
-- 2、算法教程表
-- ----------------------------
create table sys_algo_tutorial (
  tutorial_id         int(6)        not null auto_increment      comment '教程id',
  tutorial_name       varchar(80)   not null                     comment '教程名称',
  algo_id         int(6)            not null     comment '算法id',
  tutorial_content  mediumtext      default null               comment '教程内容',
  create_by         varchar(30)     default ''                 comment '创建人',
  create_time 	    datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新人',
  update_time       datetime                                   comment '更新时间',
  primary key (tutorial_id)
) engine=innodb auto_increment=1 comment = '算法教程表';
```

## 标签表
```bash
-- ----------------------------
-- 5、标签表
-- ----------------------------
create table sys_tag (
  tag_id         int(6)        not null auto_increment      comment '标签id',
  tag_name       varchar(20)   not null                     comment '标签名称',
  primary key (tag_id)
) engine=innodb auto_increment=1 comment = '标签表';

```

## 算法-标签表

```bash
-- ----------------------------
-- 6、算法-标签表
-- ----------------------------
create table sys_algo_tag
(
  algo_id   int(6) not null comment '算法ID',
  tag_id    int(6) not null comment '标签ID',
  primary key (algo_id, tag_id)
) engine=innodb comment = '算法与标签关联表';
```

# 公共数据
## 数据列表
```bash
-- ----------------------------
-- 7、公共数据表
-- ----------------------------
create table sys_dataset (
  dataset_id         int(6)        not null auto_increment      comment '数据id',
  dataset_name       varchar(80)   not null                     comment '数据名称',
  dataset_desc       varchar(200)  default null                 comment '数据简介',
  dataset_content    mediumtext    default null                 comment '数据详情',
  create_by         varchar(30)     default ''                 comment '创建人',
  create_time 	    datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新人',
  update_time       datetime                                   comment '更新时间',
  primary key (dataset_id)
) engine=innodb auto_increment=1 comment = '数据表';
```
## 数据-标签表
```bash
create table sys_dataset_tag
(
  dataset_id   int(6) not null comment '数据ID',
  tag_id    int(6) not null comment '标签ID',
  primary key (dataset_id, tag_id)
) engine=innodb comment = '数据与标签关联表';
```

# 文献资料
## 文献列表
```bash
-- ----------------------------
-- 8、文献表
-- ----------------------------

create table sys_ref (
  ref_id         int(6)        not null auto_increment      comment '文献id',
  ref_title      text          not null                     comment '文献英文标题',
  ref_title_zh   text          default null                     comment '文献中文标题',
  ref_doi        text          default null                 comment '文献DOI',
  ref_abs        text          default null                 comment '文献摘要',
  create_by         varchar(30)     default ''                 comment '创建人',
  create_time 	    datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新人',
  update_time       datetime                                   comment '更新时间',
  primary key (ref_id)
) engine=innodb auto_increment=1 comment = '文献表';
```

## 文献-标签表
```bash
create table sys_ref_tag
(
  ref_id   int(6) not null comment '文献ID',
  tag_id    int(6) not null comment '标签ID',
  primary key (ref_id, tag_id)
) engine=innodb comment = '文献与标签关联表';
```


## 文献分析
```bash
-- ----------------------------
-- 9、文献分析表
-- ----------------------------
create table sys_ref_article (
  article_id         int(6)        not null auto_increment      comment '文章id',
  article_name       varchar(80)   not null                     comment '文章名称',
  ref_id         int(6)            not null     comment '文献id',
  article_content   mediumtext      default null               comment '文章内容',
  create_by         varchar(30)     default ''                 comment '创建人',
  create_time 	    datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新人',
  update_time       datetime                                   comment '更新时间',
  primary key (article_id)
) engine=innodb auto_increment=1 comment = '文献分析表';
```
## 文献复现
```bash
-- ----------------------------
-- 9、文献复现表
-- ----------------------------
create table sys_ref_reprod (
  reprod_id         int(6)        not null auto_increment      comment '复现id',
  reprod_name       varchar(80)   not null                     comment '复现名称',
  ref_id           int(6)            not null     comment '文献id',
  reprod_content   mediumtext      default null               comment '复现内容',
  create_by         varchar(30)     default ''                 comment '创建人',
  create_time 	    datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新人',
  update_time       datetime                                   comment '更新时间',
  primary key (reprod_id)
) engine=innodb auto_increment=1 comment = '文献复现表';
```

# 研究项目
## 项目列表
```bash
-- ----------------------------
-- 10、项目表
-- ----------------------------

create table sys_project (
  project_id         int(6)        not null auto_increment      comment '项目id',
  project_title      varchar(40)   not null                     comment '项目标题',
  user_id            bigint(20)    not null                     comment '项目负责人',
  project_desc       TEXT          default null                 comment '项目描述',
  create_by         varchar(30)     default ''                 comment '创建人',
  create_time 	    datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新人',
  update_time       datetime                                   comment '更新时间',
  primary key (project_id)
) engine=innodb auto_increment=1 comment = '项目表';
```
## 项目成员
```bash
create table sys_project_member
(
  project_id   int(6) not null comment '数据ID',
  user_id    bigint(20) not null comment '标签ID',
  member_role varchar(200) default null comment '项目分工',
  primary key (project_id, user_id)
) engine=innodb comment = '项目与用户关联表';
```
## 项目文档
```bash
-- ----------------------------
-- 9、项目文档表
-- ----------------------------
create table sys_project_doc (
  doc_id         int(6)        not null auto_increment      comment '文档id',
  doc_name       varchar(80)   not null                     comment '文档名称',
  project_id           int(6)            not null     comment '文献id',
  doc_desc      varchar(200)   not null                     comment '文档简介',
  doc_content   mediumtext      default null               comment '文档内容',
  create_by         varchar(30)     default ''                 comment '创建人',
  create_time 	    datetime                                   comment '创建时间',
  update_by         varchar(30)     default ''                 comment '更新人',
  update_time       datetime                                   comment '更新时间',
  primary key (project_doc)
) engine=innodb auto_increment=1 comment = '项目文档表';
```

## 项目-标签表
```bash
create table sys_project_tag
(
  project_id   int(6) not null comment '项目ID',
  tag_id    int(6) not null comment '标签ID',
  primary key (project_id, tag_id)
) engine=innodb comment = '数据与标签关联表';
```

# 实用工具
## 工具列表
## 工具详情
