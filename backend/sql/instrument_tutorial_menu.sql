-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('仪器教程', '1', '1', 'instrument_tutorial', 'system/instrument_tutorial/index', 1, 0, 'C', '0', '0', 'system:instrument_tutorial:list', '#', 'admin', sysdate(), '', null, '仪器教程菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('仪器教程查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'system:instrument_tutorial:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('仪器教程新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'system:instrument_tutorial:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('仪器教程修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'system:instrument_tutorial:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('仪器教程删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'system:instrument_tutorial:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('仪器教程导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'system:instrument_tutorial:export',       '#', 'admin', sysdate(), '', null, '');
