import request from '@/utils/request'

// 查询仪器教程列表
export function listDevice_tutorial(query) {
  return request({
    url: '/system/device_tutorial/list',
    method: 'get',
    params: query
  })
}

// 查询仪器教程详细
export function getDevice_tutorial(tutorialId) {
  return request({
    url: '/system/device_tutorial/' + tutorialId,
    method: 'get'
  })
}

// 新增仪器教程
export function addDevice_tutorial(data) {
  return request({
    url: '/system/device_tutorial',
    method: 'post',
    data: data
  })
}

// 修改仪器教程
export function updateDevice_tutorial(data) {
  return request({
    url: '/system/device_tutorial',
    method: 'put',
    data: data
  })
}

// 删除仪器教程
export function delDevice_tutorial(tutorialId) {
  return request({
    url: '/system/device_tutorial/' + tutorialId,
    method: 'delete'
  })
}
