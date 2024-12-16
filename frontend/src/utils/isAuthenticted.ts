export const isAuthenticated = (): boolean => {
  const refresh_token = localStorage.getItem('refresh_token')
  return Boolean(refresh_token)
}
