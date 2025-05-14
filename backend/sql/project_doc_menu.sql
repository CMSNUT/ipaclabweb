-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('项目文档', '1', '1', 'project_doc', 'system/project_doc/index', 1, 0, 'C', '0', '0', 'system:project_doc:list', '#', 'admin', sysdate(), '', null, '项目文档菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('项目文档查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'system:project_doc:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('项目文档新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'system:project_doc:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('项目文档修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'system:project_doc:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('项目文档删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'system:project_doc:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('项目文档导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'system:project_doc:export',       '#', 'admin', sysdate(), '', null, '');
