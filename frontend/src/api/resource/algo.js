import request from '@/utils/request'

// 查询程序管理列表
export function listAlgo(query) {
  return request({
    url: '/resource/algo/list',
    method: 'get',
    params: query
  })
}

// 查询程序管理详细
export function getAlgo(algoId) {
  return request({
    url: '/resource/algo/' + algoId,
    method: 'get'
  })
}

// 新增程序管理
export function addAlgo(data) {
  return request({
    url: '/resource/algo',
    method: 'post',
    data: data
  })
}

// 修改程序管理
export function updateAlgo(data) {
  return request({
    url: '/resource/algo',
    method: 'put',
    data: data
  })
}

// 删除程序管理
export function delAlgo(algoId) {
  return request({
    url: '/resource/algo/' + algoId,
    method: 'delete'
  })
}
