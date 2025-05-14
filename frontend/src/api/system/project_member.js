import request from '@/utils/request'

// 查询项目与用户关联列表
export function listProject_member(query) {
  return request({
    url: '/system/project_member/list',
    method: 'get',
    params: query
  })
}

// 查询项目与用户关联详细
export function getProject_member(projectId) {
  return request({
    url: '/system/project_member/' + projectId,
    method: 'get'
  })
}

// 新增项目与用户关联
export function addProject_member(data) {
  return request({
    url: '/system/project_member',
    method: 'post',
    data: data
  })
}

// 修改项目与用户关联
export function updateProject_member(data) {
  return request({
    url: '/system/project_member',
    method: 'put',
    data: data
  })
}

// 删除项目与用户关联
export function delProject_member(projectId) {
  return request({
    url: '/system/project_member/' + projectId,
    method: 'delete'
  })
}
