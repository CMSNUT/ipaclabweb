-- ----------------------------
-- 1、标签表
-- ----------------------------
create table res_tag (
  tag_id           int(6)          not null auto_increment    comment '标签id',
  tag_label         varchar(20)    unique not null             comment '标签名称',
  tag_value         varchar(20)    unique not null             comment '标签值',
  parent_id        int(6)          default null               comment '父标签id',
  create_by     varchar(15)     default ''                 comment '创建者',
  create_time   datetime                                   comment '创建时间',
  update_by     varchar(15)     default ''			       comment '更新者',
  update_time   datetime                                   comment '更新时间',
  primary key (tag_id)
) engine=innodb auto_increment=1 comment = '标签表';

-- ----------------------------
-- 2、仪器表
-- ----------------------------
create table res_device
(
  device_id       int(6)      not null auto_increment    comment '仪器ID',
  device_name     varchar(64) unique not null            comment '仪器名称',
  device_img    varchar(100)  default null               comment '仪器图片',
  create_by     varchar(15)     default ''                 comment '创建者',
  create_time   datetime                                   comment '创建时间',
  update_by     varchar(15)     default ''			       comment '更新者',
  update_time   datetime                                   comment '更新时间',
  primary key (device_id)
) engine=innodb comment = '仪器表';

-- ----------------------------
-- 3、程序表
-- ----------------------------
create table res_algo
(
  algo_id       int(6)      not null auto_increment    comment '程序ID',
  algo_name     varchar(64) unique not null            comment '程序名称',
  algo_desc     mediumtext      null                   comment '程序介绍',
  algo_type     char(1)         default '0'            comment '程序类型',
  algo_lang     char(1)         default '0'            comment '编程语言',
  create_by     varchar(15)     default ''                 comment '创建者',
  create_time   datetime                                   comment '创建时间',
  update_by     varchar(15)     default ''			       comment '更新者',
  update_time   datetime                                   comment '更新时间',
  primary key (algo_id)
) engine=innodb comment = '程序表';

-- ----------------------------
-- 4、程序标签表
-- ----------------------------
CREATE TABLE res_algo_tag (
  algo_id int(6)      not null comment '程序ID',
  tag_id int(6)      not null comment '标签ID',
  create_by     varchar(15)     default ''                 comment '创建者',
  create_time   datetime                                   comment '创建时间',
  update_by     varchar(15)     default ''			       comment '更新者',
  update_time   datetime                                   comment '更新时间',
  PRIMARY KEY (algo_id, tag_id),
  FOREIGN KEY (algo_id) REFERENCES res_algo(algo_id),
  FOREIGN KEY (tag_id) REFERENCES res_tag(tag_id)
)engine=innodb comment = '程序标签关联表';