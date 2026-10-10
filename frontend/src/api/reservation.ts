import request from '@/utils/request'

/**
 * 创建预约
 */
export function createReservationApi(data: Record<string, any>) {
    return request({
        url: '/api/reservation',
        method: 'post',
        data
    })
}


/**
 * 查询预约记录
 */
export function getReservationPageList(params: Record<string, any>) {
    return request({
        url: '/api/reservation/list',
        method: 'get',
        params
    })
}

/**
 * 取消预约
 */
export function cancelReservationApi(id: Number) {
    return request({
        url: `/api/reservation/${id}/cancel`,
        method: 'put'
    })
}

/**
 * 审核预约
 */
export function auditReservationApi(id: Number, status: Number) {
    return request({
        url: `/api/reservation/${id}/audit`,
        method: 'put',
        data: { status }
    })
}