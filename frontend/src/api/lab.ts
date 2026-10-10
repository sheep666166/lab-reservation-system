import request from '@/utils/request'

/** 分页查询实验室 */
export function getLabPageList(params: Record<string, any>) {
    return request({
        url: '/api/lab/list',
        method: 'get',
        params
    })
}

/** 新增实验室 */
export function createLabApi(data: Record<string, any>) {
    return request({
        url: '/api/lab',
        method: 'post',
        data
    })
}

/** 修改实验室 */
export function updateLabApi(lab_id: number, data: Record<string, any>) {
    return request({
        url: `/api/lab/${lab_id}`,
        method: 'put',
        data
    })
}

/** 删除实验室 */
export function deleteLabApi(lab_id: number) {
    return request({
        url: `/api/lab/${lab_id}`,
        method: 'delete'
    })
}

/**
 * 根据ID查询实验室详情
 * @param lab_id 实验室ID
 * @returns
 */
export function getLab(lab_id: number) {
    return request({
        url: `/api/lab/${lab_id}`,
        method: 'get'
    })
}