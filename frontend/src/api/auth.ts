import request from '@/utils/request'

/**
 * 登录请求
 */
export function loginApi(data: { username: string; password: string }) {
  return request({
    url: '/api/auth/login',
    method: 'post',
    data
  })
}

export function registerApi(data: { username: string; password: string; email?: string }) {
  return request({
    url: '/api/auth/register',
    method: 'post',
    data
  })
}