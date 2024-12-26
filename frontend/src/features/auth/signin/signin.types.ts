import {
  InitialState,
  SuccessResponse,
  ErrorResponse
} from 'FeatureTypes';

type SigninDataResponse = {
  access_token: string | null;
  refresh_token: string | null;
}

type SigninErrorsResponse = {
  non_field_errors?: string[]
}

type RefreshTokenDataResponse = {
  access_token: string;
}

type RefreshTokenErrorsResponse = {
  access_token?: string[];
  non_field_errors?: string[];
}

export interface SigninInitialState extends InitialState<
  SigninDataResponse,
  SigninErrorsResponse | null,
  {} | null
> { }

export interface SigninSuccessResponse extends SuccessResponse<SigninDataResponse> { }

export interface SigninErrorResponse extends ErrorResponse<
  SigninErrorsResponse
> { }

export interface RefreshTokenSuccessResponse extends SuccessResponse<RefreshTokenDataResponse> { }

export interface RefreshTokenErrorResponse extends ErrorResponse<
  RefreshTokenErrorsResponse
> { }
