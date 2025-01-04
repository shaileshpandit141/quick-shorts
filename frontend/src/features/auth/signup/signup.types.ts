// Import necessary types from FeatureTypes
import {
  InitialState,
  SuccessResponse,
  ErrorResponse
} from 'FeatureTypes';

/**
 * Type definition for signup response data
 */
type SignupData = {
  detail: string;
}

/**
 * Type definition for possible signup form validation errors
 */
type SignupErrors = {
  email?: string[];
  password?: string[];
  confirm_password?: string[];
  non_field_errors?: string[];
}

/**
 * Interface for signup initial state
 */
export interface SignupInitialState extends InitialState<
  SignupData | null,
  SignupErrors | null,
  {} | null
> { }

/**
 * Interface for successful signup response
 */
export interface SignupSuccessResponse extends SuccessResponse<
  SignupData
> { }

/**
 * Interface for signup error response
 */
export interface SignupErrorResponse extends ErrorResponse<
  SignupErrors
> { }
