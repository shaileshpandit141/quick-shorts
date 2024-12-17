export declare module 'FeatureTypes' {
  // Generic structure for state initialization
  export interface InitialState<
    DATA = Record<string, any>,
    ERRORS = Record<string, string[]>,
    MATA = Record<string, any>
  > {
    status: 'idle' | 'loading' | 'succeeded' | 'failed';
    message: string;
    data: DATA;
    errors: ERRORS;
    meta: MATA | null;
  }

  // Success response type
  export interface SuccessResponse<
    DATA = Record<string, any>,
    META = Record<string, any>
  > {
    status: 'succeeded';
    message: string;
    data: DATA;
    meta: META | null;
  }

  // Error response type
  export interface ErrorResponse<
    ERRORS = Record<string, string[]>
  > {
    status: 'failed';
    message: string;
    errors: ERRORS | null;
  }

  // Axios catch error structure
  export interface CatchAxiosError {
    response?: {
      data: ErrorResponse;
    };
    message?: string;
  }
}
