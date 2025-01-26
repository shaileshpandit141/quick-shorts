/**
 * Credentials for user sign in
 */
export interface SigninCredentials {
  email: string
  password: string
}

/**
 * Credentials for new user registration
 */
export interface SignupCredentials {
  email: string
  password: string
  confirm_password: string
}

/**
 * Credentials for user sign out
 */
export interface SignoutCredentials {
  refresh_token: string
}

/**
 * Credentials for password reset request
 */
export interface PasswordResetCredentials {
  email: string
}

/**
 * Credentials to confirm and set new password
 */
export interface ConfirmPasswordResetCredentials {
  uid: string
  token: string
  new_password1: string
  new_password2: string
}

/**
 * Credentials for email verification
 */
export interface VerifyEmailCredentials {
  key: string
}

/**
 * Credentials for resending verification email
 */
export interface RsendVerificationEmailCredentials { }

/**
 * Credentials for refreshing authentication token
 */
export interface RefreshTokenCredentials {
  refresh_token: string
}
