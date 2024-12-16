export declare module 'FeatureTypes' {
  // Generic structure for state initialization
  export interface InitialState<DATA = Record<string, any>, MATA = Record<string, any>> {
    status: 'idle' | 'loading' | 'succeeded' | 'failed';
    message: string;
    data: DATA;
    errors: Record<string, any> | null;
    meta: MATA | null;
  }

  // Success response type
  export interface SuccessResponse<DATA = Record<string, any>, META = Record<string, any>> {
    status: 'succeeded';
    message: string;
    data: DATA;
    meta: META | null;
  }

  // Error response type
  export interface ErrorResponse<FIELDS = Record<string, string[]>> {
    status: 'failed';
    message: string;
    errors: ?FIELDS & {
      non_field_errors?: string[];
    };
  }


  // Axios catch error structure
  export interface CatchAxiosError {
    response?: {
      data: ErrorResponse;
    };
    message?: string;
  }
}
