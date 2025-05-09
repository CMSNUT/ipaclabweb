import request from '@/utils/request'

// 查询仪器信息列表
export function listDevice(query) {
  return request({
    url: '/system/device/list',
    method: 'get',
    params: query
  })
}

// 查询仪器信息详细
export function getDevice(deviceId) {
  return request({
    url: '/system/device/' + deviceId,
    method: 'get'
  })
}

// 新增仪器信息
export function addDevice(data) {
  return request({
    url: '/system/device',
    method: 'post',
    data: data
  })
}

// 修改仪器信息
export function updateDevice(data) {
  return request({
    url: '/system/device',
    method: 'put',
    data: data
  })
}

// 删除仪器信息
export function delDevice(deviceId) {
  return request({
    url: '/system/device/' + deviceId,
    method: 'delete'
  })
}
