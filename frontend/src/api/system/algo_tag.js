import request from '@/utils/request'

// 查询算法与标签关联列表
export function listAlgo_tag(query) {
  return request({
    url: '/system/algo_tag/list',
    method: 'get',
    params: query
  })
}

// 查询算法与标签关联详细
export function getAlgo_tag(algoId) {
  return request({
    url: '/system/algo_tag/' + algoId,
    method: 'get'
  })
}

// 新增算法与标签关联
export function addAlgo_tag(data) {
  return request({
    url: '/system/algo_tag',
    method: 'post',
    data: data
  })
}

// 修改算法与标签关联
export function updateAlgo_tag(data) {
  return request({
    url: '/system/algo_tag',
    method: 'put',
    data: data
  })
}

// 删除算法与标签关联
export function delAlgo_tag(algoId) {
  return request({
    url: '/system/algo_tag/' + algoId,
    method: 'delete'
  })
}
