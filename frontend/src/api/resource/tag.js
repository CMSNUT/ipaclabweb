import request from '@/utils/request'

// 查询标签管理列表
export function listTag(query) {
  return request({
    url: '/resource/tag/list',
    method: 'get',
    params: query
  })
}

// 查询标签管理详细
export function getTag(tagId) {
  return request({
    url: '/resource/tag/' + tagId,
    method: 'get'
  })
}

// 新增标签管理
export function addTag(data) {
  return request({
    url: '/resource/tag',
    method: 'post',
    data: data
  })
}

// 修改标签管理
export function updateTag(data) {
  return request({
    url: '/resource/tag',
    method: 'put',
    data: data
  })
}

// 删除标签管理
export function delTag(tagId) {
  return request({
    url: '/resource/tag/' + tagId,
    method: 'delete'
  })
}
