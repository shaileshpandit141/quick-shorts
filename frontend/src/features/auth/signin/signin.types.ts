import {
  InitialState,
  SuccessResponse,
  ErrorResponse
} from 'FeatureTypes';

export interface SigninInitialState extends InitialState<
  {
    access_token: string | null;
    refresh_token: string | null;
  },
  {
    non_field_errors?: string[]
  },
  {} | null
> { }

export interface SigninSuccessResponse extends SuccessResponse<{
  access_token: string;
  refresh_token: string;
}> { }

export interface RefreshTokenSuccessResponse extends SuccessResponse<{
  access_token: string;
}> { }

export interface SigninErrorResponse extends ErrorResponse<{
  non_field_errors?: string[];
}> { }

export interface RefreshTokenErrorResponse extends ErrorResponse<{
  access_token?: string[];
  non_field_errors?: string[];
}> { }
