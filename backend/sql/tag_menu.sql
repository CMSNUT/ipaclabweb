-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('标签管理', '1', '1', 'tag', 'system/tag/index', 1, 0, 'C', '0', '0', 'system:tag:list', '#', 'admin', sysdate(), '', null, '标签管理菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('标签管理查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'system:tag:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('标签管理新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'system:tag:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('标签管理修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'system:tag:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('标签管理删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'system:tag:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('标签管理导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'system:tag:export',       '#', 'admin', sysdate(), '', null, '');
