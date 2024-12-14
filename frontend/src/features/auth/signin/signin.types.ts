export interface SigninCredentials {
  email: string
  password: string
}

export interface SigninIntitlState {
  status: 'idle' | 'loading' | 'succeeded' | 'failed'
  message: string
  data: {
    access_token: string | null
    refresh_token: string | null
  }
  errors: {} | null
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

export interface ErrorResponse {
  status: 'failed';
  message: string;
  errors: {
    [key: string]: string[];
  };
}

export interface CatchErrorResponse {
  response?: {
    data: ErrorResponse
  }
  message?: ErrorResponse
}
