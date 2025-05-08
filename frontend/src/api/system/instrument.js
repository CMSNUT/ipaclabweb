import request from '@/utils/request'

// 查询仪器信息列表
export function listInstrument(query) {
  return request({
    url: '/system/instrument/list',
    method: 'get',
    params: query
  })
}

// 查询仪器信息详细
export function getInstrument(instrumentId) {
  return request({
    url: '/system/instrument/' + instrumentId,
    method: 'get'
  })
}

// 新增仪器信息
export function addInstrument(data) {
  return request({
    url: '/system/instrument',
    method: 'post',
    data: data
  })
}

// 修改仪器信息
export function updateInstrument(data) {
  return request({
    url: '/system/instrument',
    method: 'put',
    data: data
  })
}

// 删除仪器信息
export function delInstrument(instrumentId) {
  return request({
    url: '/system/instrument/' + instrumentId,
    method: 'delete'
  })
}
