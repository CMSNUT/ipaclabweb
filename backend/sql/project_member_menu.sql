-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('项目与用户关联', '1', '1', 'project_member', 'system/project_member/index', 1, 0, 'C', '0', '0', 'system:project_member:list', '#', 'admin', sysdate(), '', null, '项目与用户关联菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('项目与用户关联查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'system:project_member:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('项目与用户关联新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'system:project_member:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('项目与用户关联修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'system:project_member:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('项目与用户关联删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'system:project_member:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('项目与用户关联导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'system:project_member:export',       '#', 'admin', sysdate(), '', null, '');
