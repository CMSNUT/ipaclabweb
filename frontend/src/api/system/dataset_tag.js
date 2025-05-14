import request from '@/utils/request'

// 查询数据与标签关联列表
export function listDataset_tag(query) {
  return request({
    url: '/system/dataset_tag/list',
    method: 'get',
    params: query
  })
}

// 查询数据与标签关联详细
export function getDataset_tag(datasetId) {
  return request({
    url: '/system/dataset_tag/' + datasetId,
    method: 'get'
  })
}

// 新增数据与标签关联
export function addDataset_tag(data) {
  return request({
    url: '/system/dataset_tag',
    method: 'post',
    data: data
  })
}

// 修改数据与标签关联
export function updateDataset_tag(data) {
  return request({
    url: '/system/dataset_tag',
    method: 'put',
    data: data
  })
}

// 删除数据与标签关联
export function delDataset_tag(datasetId) {
  return request({
    url: '/system/dataset_tag/' + datasetId,
    method: 'delete'
  })
}
