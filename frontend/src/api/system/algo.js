import request from '@/utils/request'

// 查询算法管理列表
export function listAlgo(query) {
  return request({
    url: '/system/algo/list',
    method: 'get',
    params: query
  })
}

// 查询算法管理详细
export function getAlgo(algoId) {
  return request({
    url: '/system/algo/' + algoId,
    method: 'get'
  })
}

// 新增算法管理
export function addAlgo(data) {
  return request({
    url: '/system/algo',
    method: 'post',
    data: data
  })
}

// 修改算法管理
export function updateAlgo(data) {
  return request({
    url: '/system/algo',
    method: 'put',
    data: data
  })
}

// 删除算法管理
export function delAlgo(algoId) {
  return request({
    url: '/system/algo/' + algoId,
    method: 'delete'
  })
}
