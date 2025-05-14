-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文献管理', '1', '1', 'ref', 'system/ref/index', 1, 0, 'C', '0', '0', 'system:ref:list', '#', 'admin', sysdate(), '', null, '文献管理菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文献管理查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'system:ref:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文献管理新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'system:ref:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文献管理修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'system:ref:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文献管理删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'system:ref:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文献管理导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'system:ref:export',       '#', 'admin', sysdate(), '', null, '');
