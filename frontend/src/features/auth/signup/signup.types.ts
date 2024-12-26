import {
  InitialState,
  SuccessResponse,
  ErrorResponse
} from 'FeatureTypes';

type SignupData = {
  detail: string;
}

type SignupErrors = {
  email?: string[];
  password?: string[];
  confirm_password?: string[];
  non_field_errors?: string[]
}

export interface SignupInitialState extends InitialState<
  SignupData | null,
  SignupErrors | null,
  {} | null
> { }

export interface SignupSuccessResponse extends SuccessResponse<
  SignupData
> { }

export interface SignupErrorResponse extends ErrorResponse<
  SignupErrors
> { }
