import request from '@/utils/request'

// 查询文献分析列表
export function listRef_article(query) {
  return request({
    url: '/system/ref_article/list',
    method: 'get',
    params: query
  })
}

// 查询文献分析详细
export function getRef_article(articleId) {
  return request({
    url: '/system/ref_article/' + articleId,
    method: 'get'
  })
}

// 新增文献分析
export function addRef_article(data) {
  return request({
    url: '/system/ref_article',
    method: 'post',
    data: data
  })
}

// 修改文献分析
export function updateRef_article(data) {
  return request({
    url: '/system/ref_article',
    method: 'put',
    data: data
  })
}

// 删除文献分析
export function delRef_article(articleId) {
  return request({
    url: '/system/ref_article/' + articleId,
    method: 'delete'
  })
}
