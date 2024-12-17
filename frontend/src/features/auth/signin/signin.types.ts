import {
  InitialState,
  SuccessResponse,
  ErrorResponse
} from 'FeatureTypes';

export interface SigninIntitlState extends InitialState<
  {
    access_token: string | null;
    refresh_token: string | null;
  },
  {
    email?: string[];
    non_field_errors?: string[]
    password?: string[];
  }
> { }

export interface SigninSuccessResponse extends SuccessResponse<{
  access_token: string;
  refresh_token: string;
}> { }

export interface RefreshTokenSuccessResponse extends SuccessResponse<{
  access_token: string;
}> { }

export interface SigninErrorResponse extends ErrorResponse<{
  email?: string[];
  non_field_errors?: string[];
  password?: string[];
}> { }

export interface RefreshTokenErrorResponse extends ErrorResponse<{
  access_token?: string[];
  non_field_errors?: string[];
}> { }
