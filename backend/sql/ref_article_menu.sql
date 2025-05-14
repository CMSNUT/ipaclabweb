-- 菜单 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文献分析', '1', '1', 'ref_article', 'system/ref_article/index', 1, 0, 'C', '0', '0', 'system:ref_article:list', '#', 'admin', sysdate(), '', null, '文献分析菜单');

-- 按钮父菜单ID
SELECT @parentId := LAST_INSERT_ID();

-- 按钮 SQL
insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文献分析查询', @parentId, '1',  '#', '', 1, 0, 'F', '0', '0', 'system:ref_article:query',        '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文献分析新增', @parentId, '2',  '#', '', 1, 0, 'F', '0', '0', 'system:ref_article:add',          '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文献分析修改', @parentId, '3',  '#', '', 1, 0, 'F', '0', '0', 'system:ref_article:edit',         '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文献分析删除', @parentId, '4',  '#', '', 1, 0, 'F', '0', '0', 'system:ref_article:remove',       '#', 'admin', sysdate(), '', null, '');

insert into sys_menu (menu_name, parent_id, order_num, path, component, is_frame, is_cache, menu_type, visible, status, perms, icon, create_by, create_time, update_by, update_time, remark)
values('文献分析导出', @parentId, '5',  '#', '', 1, 0, 'F', '0', '0', 'system:ref_article:export',       '#', 'admin', sysdate(), '', null, '');
