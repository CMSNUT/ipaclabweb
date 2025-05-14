import request from '@/utils/request'

// 查询项目文档列表
export function listProject_doc(query) {
  return request({
    url: '/system/project_doc/list',
    method: 'get',
    params: query
  })
}

// 查询项目文档详细
export function getProject_doc(docId) {
  return request({
    url: '/system/project_doc/' + docId,
    method: 'get'
  })
}

// 新增项目文档
export function addProject_doc(data) {
  return request({
    url: '/system/project_doc',
    method: 'post',
    data: data
  })
}

// 修改项目文档
export function updateProject_doc(data) {
  return request({
    url: '/system/project_doc',
    method: 'put',
    data: data
  })
}

// 删除项目文档
export function delProject_doc(docId) {
  return request({
    url: '/system/project_doc/' + docId,
    method: 'delete'
  })
}
