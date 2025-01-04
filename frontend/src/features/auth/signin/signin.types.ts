import {
  InitialState,
  SuccessResponse,
  ErrorResponse
} from 'FeatureTypes';

/**
 * Type definitions for sign-in response data
 */
type SigninDataResponse = {
  access_token: string | null;    // JWT access token
  refresh_token: string | null;   // JWT refresh token
}

/**
 * Type for sign-in error response
 */
type SigninErrorsResponse = {
  non_field_errors?: string[]     // General authentication errors
}

/**
 * Type for refresh token response data
 */
type RefreshTokenDataResponse = {
  access_token: string;           // New JWT access token
}

/**
 * Type for refresh token error response
 */
type RefreshTokenErrorsResponse = {
  access_token?: string[];        // Access token related errors
  non_field_errors?: string[];    // General refresh token errors
}

/**
 * Interface for initial sign-in state
 */
export interface SigninInitialState extends InitialState<
  SigninDataResponse,
  SigninErrorsResponse | null,
  {} | null
> { }

/**
 * Interface for successful sign-in response
 */
export interface SigninSuccessResponse extends SuccessResponse<SigninDataResponse> { }

/**
 * Interface for sign-in error response
 */
export interface SigninErrorResponse extends ErrorResponse<
  SigninErrorsResponse
> { }

/**
 * Interface for successful token refresh response
 */
export interface RefreshTokenSuccessResponse extends SuccessResponse<RefreshTokenDataResponse> { }

/**
 * Interface for token refresh error response
 */
export interface RefreshTokenErrorResponse extends ErrorResponse<
  RefreshTokenErrorsResponse
> { }
