/**
 * Credentials for user sign in
 * @property {string} email - The user's email address.
 * @property {string} password - The user's password.
 */
export interface SigninCredentials {
  email: string
  password: string
}

/**
 * Credentials for new user registration
 * @property {string} email - The user's email address.
 * @property {string} password - The user's password.
 * @property {string} confirm_password - Confirmation of the user's password.
 */
export interface SignupCredentials {
  email: string
  password: string
  confirm_password: string
}

/**
 * Credentials for user sign out
 * @property {string} refresh_token - The token used to refresh authentication.
 */
export interface SignoutCredentials {
  refresh_token: string
}

/**
 * Credentials for refreshing authentication token
 * @property {string} refresh_token - The token used to refresh authentication.
 */
export interface RefreshTokenCredentials {
  refresh_token: string
}

/**
 * Credentials for verifying user account
 * @property {string} token - The token used to verify the user account.
 */
export interface VerifyUserAccountCredentials {
  token: string;
}
