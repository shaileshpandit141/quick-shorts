export declare module 'FeatureTypes' {
  /**
   * Generic state structure with customizable data types
   * @template DATA - Type for the data property (defaults to Record<string,any>)
   * @template ERRORS - Type for the errors property (defaults to Record<string,string[]>)
   * @template META - Type for the meta property (defaults to Record<string,any>)
   */
  export interface InitialState<
    DATA = Record<string, any>,
    ERRORS = Record<string, string[]>,
    META = Record<string, any>
  > {
    status: 'idle' | 'loading' | 'succeeded' | 'failed';
    message: string;
    data: DATA;
    errors: ERRORS;
    meta: META;
  }

  /**
   * Success response interface for API calls
   * @template DATA - Type for returned data (defaults to Record<string,any>)
   * @template META - Type for metadata (defaults to Record<string,any>)
   */
  export interface SuccessResponse<
    DATA = Record<string, any>,
    META = Record<string, any>
  > {
    status: 'succeeded';
    message: string;
    data: DATA;
    meta: META;
  }

  /**
   * Error response interface for failed API calls
   * @template ERRORS - Type for error details (defaults to Record<string,string[]>)
   */
  export interface ErrorResponse<
    ERRORS = Record<string, string[]>
  > {
    status: 'failed';
    message: string;
    errors: ERRORS;
  }

  /**
   * Axios error catch structure containing error response data
   */
  export interface CatchAxiosError {
    response?: {
      data: ErrorResponse;
    };
    message?: string;
  }
}
