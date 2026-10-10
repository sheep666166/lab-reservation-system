import request from '@/utils/request'

/**
 * 分页模糊查询列表
 */
export function getEquipmentPageList(params: Record<string, any>) {
    return request({
        url: '/api/equipment/list',
        method: 'get',
        params
    })
}

/**
 * 新增
 */
export function createEquipmentApi(data: Record<string, any>) {
    return request({
        url: '/api/equipment',
        method: 'post',
        data
    })
}

/**
 * 修改
 */
export function updateEquipmentApi(equipment_id: string, data: Record<string, any>) {
    return request({
        url: `/api/equipment/${equipment_id}`,
        method: 'put',
        data
    })
}

/**
 * 删除
 */
export function deleteEquipmentApi(equipment_id: string) {
    return request({
        url: `/api/equipment/${equipment_id}`,
        method: 'delete'
    })
}