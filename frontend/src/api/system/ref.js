import request from '@/utils/request'

// 查询文献管理列表
export function listRef(query) {
  return request({
    url: '/system/ref/list',
    method: 'get',
    params: query
  })
}

// 查询文献管理详细
export function getRef(refId) {
  return request({
    url: '/system/ref/' + refId,
    method: 'get'
  })
}

// 新增文献管理
export function addRef(data) {
  return request({
    url: '/system/ref',
    method: 'post',
    data: data
  })
}

// 修改文献管理
export function updateRef(data) {
  return request({
    url: '/system/ref',
    method: 'put',
    data: data
  })
}

// 删除文献管理
export function delRef(refId) {
  return request({
    url: '/system/ref/' + refId,
    method: 'delete'
  })
}
