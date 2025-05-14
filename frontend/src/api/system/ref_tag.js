import request from '@/utils/request'

// 查询文献与标签关联列表
export function listRef_tag(query) {
  return request({
    url: '/system/ref_tag/list',
    method: 'get',
    params: query
  })
}

// 查询文献与标签关联详细
export function getRef_tag(refId) {
  return request({
    url: '/system/ref_tag/' + refId,
    method: 'get'
  })
}

// 新增文献与标签关联
export function addRef_tag(data) {
  return request({
    url: '/system/ref_tag',
    method: 'post',
    data: data
  })
}

// 修改文献与标签关联
export function updateRef_tag(data) {
  return request({
    url: '/system/ref_tag',
    method: 'put',
    data: data
  })
}

// 删除文献与标签关联
export function delRef_tag(refId) {
  return request({
    url: '/system/ref_tag/' + refId,
    method: 'delete'
  })
}
