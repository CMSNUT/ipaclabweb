import request from '@/utils/request'

// 查询仪器教程列表
export function listInstrument_tutorial(query) {
  return request({
    url: '/system/instrument_tutorial/list',
    method: 'get',
    params: query
  })
}

// 查询仪器教程详细
export function getInstrument_tutorial(tutorialId) {
  return request({
    url: '/system/instrument_tutorial/' + tutorialId,
    method: 'get'
  })
}

// 新增仪器教程
export function addInstrument_tutorial(data) {
  return request({
    url: '/system/instrument_tutorial',
    method: 'post',
    data: data
  })
}

// 修改仪器教程
export function updateInstrument_tutorial(data) {
  return request({
    url: '/system/instrument_tutorial',
    method: 'put',
    data: data
  })
}

// 删除仪器教程
export function delInstrument_tutorial(tutorialId) {
  return request({
    url: '/system/instrument_tutorial/' + tutorialId,
    method: 'delete'
  })
}

// 查询仪器下拉选项
export function deptTreeSelect() {
  return request({
    url: '/system/user/deptTree',
    method: 'get'
  })
}