import request from '@/utils/request'

// 查询数据管理列表
export function listDataset(query) {
  return request({
    url: '/system/dataset/list',
    method: 'get',
    params: query
  })
}

// 查询数据管理详细
export function getDataset(datasetId) {
  return request({
    url: '/system/dataset/' + datasetId,
    method: 'get'
  })
}

// 新增数据管理
export function addDataset(data) {
  return request({
    url: '/system/dataset',
    method: 'post',
    data: data
  })
}

// 修改数据管理
export function updateDataset(data) {
  return request({
    url: '/system/dataset',
    method: 'put',
    data: data
  })
}

// 删除数据管理
export function delDataset(datasetId) {
  return request({
    url: '/system/dataset/' + datasetId,
    method: 'delete'
  })
}
