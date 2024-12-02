export interface SignupIntitlState {
  status: 'idle' | 'loading' | 'succeeded' | 'failed'
  message: string
  data: {
    detail: string
  } | null
  error: {} | null
  meta: {} | null
}

export interface SigninSuccessResponse {
  status: 'succeeded'
  message: string
  data: {
    detail: string
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
