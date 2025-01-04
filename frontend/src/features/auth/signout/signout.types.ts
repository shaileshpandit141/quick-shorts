import {
  InitialState,
  SuccessResponse,
  ErrorResponse
} from "FeatureTypes";

type SignoutData = {
  detail: string;
};

type SignoutErrors = {
  refresh_token?: string[];
  non_field_errors?: string[];
};

export interface SignoutInitialState extends InitialState<
  SignoutData | null,
  SignoutErrors | null,
  {} | null
> { }

export interface SignoutSuccessResponse extends SuccessResponse<
  SignoutData
> { }

export interface SignoutErrorResponse extends ErrorResponse<
  SignoutErrors
> { }
