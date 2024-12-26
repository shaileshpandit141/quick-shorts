import {
  InitialState,
  SuccessResponse,
  ErrorResponse
} from 'FeatureTypes';

export interface SignupInitialState extends InitialState<
  {
    detail: string | null;
  },
  {
    email?: string[];
    password?: string[];
    confirm_password?: string[];
    non_field_errors?: string[]
  },
  {} | null
> { }

export interface SignupSuccessResponse extends SuccessResponse<{
  detail: string;
}> { }

export interface SignupErrorResponse extends ErrorResponse<{
  email?: string[];
  password?: string[];
  confirm_password?: string[];
  non_field_errors?: string[]
}> { }
