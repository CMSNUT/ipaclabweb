-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('数据与标签关联', '1', '1', 'dataset_tag', 'system/dataset_tag/index', 1, 0, 'C', '0', '0', 'system:dataset_tag:list', '#', 'admin', sysdate(), '', null, '数据与标签关联菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('数据与标签关联查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'system:dataset_tag:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('数据与标签关联新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'system:dataset_tag:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('数据与标签关联修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'system:dataset_tag:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('数据与标签关联删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'system:dataset_tag:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('数据与标签关联导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'system:dataset_tag:export',       '#', 'admin', sysdate(), '', null, '');
