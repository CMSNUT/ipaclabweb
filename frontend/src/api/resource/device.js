import request from '@/utils/request'

// 查询仪器管理列表
export function listDevice(query) {
  return request({
    url: '/resource/device/list',
    method: 'get',
    params: query
  })
}

// 查询仪器管理详细
export function getDevice(deviceId) {
  return request({
    url: '/resource/device/' + deviceId,
    method: 'get'
  })
}

// 新增仪器管理
export function addDevice(data) {
  return request({
    url: '/resource/device',
    method: 'post',
    data: data
  })
}

// 修改仪器管理
export function updateDevice(data) {
  return request({
    url: '/resource/device',
    method: 'put',
    data: data
  })
}

// 删除仪器管理
export function delDevice(deviceId) {
  return request({
    url: '/resource/device/' + deviceId,
    method: 'delete'
  })
}
