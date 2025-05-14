import request from '@/utils/request'

// 查询算法教程列表
export function listAlgo_tutorial(query) {
  return request({
    url: '/system/algo_tutorial/list',
    method: 'get',
    params: query
  })
}

// 查询算法教程详细
export function getAlgo_tutorial(tutorialId) {
  return request({
    url: '/system/algo_tutorial/' + tutorialId,
    method: 'get'
  })
}

// 新增算法教程
export function addAlgo_tutorial(data) {
  return request({
    url: '/system/algo_tutorial',
    method: 'post',
    data: data
  })
}

// 修改算法教程
export function updateAlgo_tutorial(data) {
  return request({
    url: '/system/algo_tutorial',
    method: 'put',
    data: data
  })
}

// 删除算法教程
export function delAlgo_tutorial(tutorialId) {
  return request({
    url: '/system/algo_tutorial/' + tutorialId,
    method: 'delete'
  })
}
