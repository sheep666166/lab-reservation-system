// 存储token、存储用户信息、获取token、用户信息，删除token、用户信息这些作用
const TOKEN_KEY = 'token'
const USER_KEY = 'userInfo'

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY)
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token)
}

export function removeToken(): void {
  localStorage.removeItem(TOKEN_KEY)
}

export function getUserInfo(): any {
  const str = localStorage.getItem(USER_KEY)
  return str ? JSON.parse(str) : null
}

export function setUserInfo(userInfo: any): void {
  localStorage.setItem(USER_KEY, JSON.stringify(userInfo))
}

export function removeUserInfo(): void {
  localStorage.removeItem(USER_KEY)
}

// 登出
export function logout(): void {
  removeToken()
  removeUserInfo()
}
