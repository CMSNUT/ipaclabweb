import request from '@/utils/request'

// 查询程序标签关联列表
export function listAlgo_tag(query) {
  return request({
    url: '/resource/algo_tag/list',
    method: 'get',
    params: query
  })
}

// 查询程序标签关联详细
export function getAlgo_tag(algoId) {
  return request({
    url: '/resource/algo_tag/' + algoId,
    method: 'get'
  })
}

// 新增程序标签关联
export function addAlgo_tag(data) {
  return request({
    url: '/resource/algo_tag',
    method: 'post',
    data: data
  })
}

// 修改程序标签关联
export function updateAlgo_tag(data) {
  return request({
    url: '/resource/algo_tag',
    method: 'put',
    data: data
  })
}

// 删除程序标签关联
export function delAlgo_tag(algoId) {
  return request({
    url: '/resource/algo_tag/' + algoId,
    method: 'delete'
  })
}
