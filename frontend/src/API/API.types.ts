export interface SigninCredentials {
  email: string
  password: string
}

export interface SignupCredentials {
  email: string
  password: string
  confirm_password: string
}

export interface SignoutCredentials {
  refresh_token: string
}

export interface PasswordResetCredentials {
  email: string
}

export interface ConfirmPasswordResetCredentials {
  uid: string
  token: string
  new_password1: string
  new_password2: string
}

export interface VerifyEmailCredentials {
  key: string
}

export interface RsendVerificationEmailCredentials { }

export interface RefreshTokenCredentials {
  refresh_token: string
}

export interface SigninUserCredentials { }
