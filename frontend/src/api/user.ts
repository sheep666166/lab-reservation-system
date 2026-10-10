import request from '@/utils/request'

/** 获取当前用户信息 */
export function getUserInfoApi() {
    return request({
        url: '/api/user/info',
        method: 'get'
    })
}

/** 修改个人信息 */
export function updateUserInfoApi(data: Record<string, any>) {
    return request({
        url: '/api/user/update',
        method: 'put',
        data
    })
}

/**修改密码 */
export function updatePasswordApi(data: Record<string, any>) {
    return request({
        url: '/api/user/password',
        method: 'put',
        data
    })
}

/**
 * 分页模糊查询用户列表
 */
export function getUserPageList(params: Record<string, any>) {
    return request({
        url: '/api/user/list',
        method: 'get',
        params
    })
}


/**
 * 新增用户
 */
export function createUserApi(data: Record<string, any>) {
    return request({
        url: '/api/user',
        method: 'post',
        data
    })
}

/**
 * 修改用户
 */
export function updateUserApi(userId: string, data: Record<string, any>) {
    return request({
        url: `/api/user/${userId}`,
        method: 'put',
        data
    })
}

/**
 * 删除用户
 */
export function deleteUserApi(userId: string) {
    return request({
        url: `/api/user/${userId}`,
        method: 'delete'
    })
}