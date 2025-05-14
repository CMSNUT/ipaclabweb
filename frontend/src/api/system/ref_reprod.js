import request from '@/utils/request'

// 查询文献复现列表
export function listRef_reprod(query) {
  return request({
    url: '/system/ref_reprod/list',
    method: 'get',
    params: query
  })
}

// 查询文献复现详细
export function getRef_reprod(reprodId) {
  return request({
    url: '/system/ref_reprod/' + reprodId,
    method: 'get'
  })
}

// 新增文献复现
export function addRef_reprod(data) {
  return request({
    url: '/system/ref_reprod',
    method: 'post',
    data: data
  })
}

// 修改文献复现
export function updateRef_reprod(data) {
  return request({
    url: '/system/ref_reprod',
    method: 'put',
    data: data
  })
}

// 删除文献复现
export function delRef_reprod(reprodId) {
  return request({
    url: '/system/ref_reprod/' + reprodId,
    method: 'delete'
  })
}
