import request from '@/utils/request'

// 查询数据与标签关联列表
export function listProject_tag(query) {
  return request({
    url: '/system/project_tag/list',
    method: 'get',
    params: query
  })
}

// 查询数据与标签关联详细
export function getProject_tag(projectId) {
  return request({
    url: '/system/project_tag/' + projectId,
    method: 'get'
  })
}

// 新增数据与标签关联
export function addProject_tag(data) {
  return request({
    url: '/system/project_tag',
    method: 'post',
    data: data
  })
}

// 修改数据与标签关联
export function updateProject_tag(data) {
  return request({
    url: '/system/project_tag',
    method: 'put',
    data: data
  })
}

// 删除数据与标签关联
export function delProject_tag(projectId) {
  return request({
    url: '/system/project_tag/' + projectId,
    method: 'delete'
  })
}
