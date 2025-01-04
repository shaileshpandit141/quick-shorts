/**
 * Types and interfaces for handling user signout functionality
 */
import {
  InitialState,
  SuccessResponse,
  ErrorResponse
} from "FeatureTypes";

/** Response data containing signout detail message */
type SignoutData = {
  detail: string;
};

/** Possible error responses during signout */
type SignoutErrors = {
  refresh_token?: string[]; // Error if refresh token is invalid/expired
  non_field_errors?: string[]; // General errors not tied to specific fields
};

/** Initial state interface for signout feature */
export interface SignoutInitialState extends InitialState<
  SignoutData | null,
  SignoutErrors | null,
  {} | null
> { }

/** Success response interface for signout */
export interface SignoutSuccessResponse extends SuccessResponse<
  SignoutData
> { }

/** Error response interface for signout */
export interface SignoutErrorResponse extends ErrorResponse<
  SignoutErrors
> { }
