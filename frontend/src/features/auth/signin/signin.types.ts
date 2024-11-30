export interface SigninIntitlState {
  status: 'idle' | 'loading' | 'succeeded' | 'failed'
  message: string
  data: {
    access_token: string
    refresh_token: string
  } | null
  error: {} | null
  meta: {} | null
}

export interface SigninSuccessResponse {
  status: 'succeeded'
  message: string
  data: {
    access_token: string
    refresh_token: string
  }
  meta: {} | null
}

export interface RefreshTokenSuccessResponse {
  status: 'succeeded'
  message: string
  data: {
    access_token: string
  }
  meta: {} | null
}
