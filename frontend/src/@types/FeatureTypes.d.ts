export declare module "FeatureTypes" {
  export interface Pagination {
    current_page: number;
    total_pages: number;
    total_items: number;
    items_per_page: number;
    has_next: boolean;
    has_previous: boolean;
  }

  export interface Errors {
    field: string;
    code: string;
    message: string;
    details: Record<string, any> | null;
  }

  export interface RateLimit {
    limit: number;
    remaining: number;
    reset_time: string;
  }

  export interface Meta {
    request_id: string;
    timestamp: string;
    response_time: string;
    documentation_url: string;
    rate_limit: RateLimit[];
  }

  /**
   * Generic state structure with customizable data types
   * @template DATA - Type for the data property (defaults to Record<string,any>)
   * @template ERRORS - Type for the errors property (defaults to Record<string,string[]>)
   * @template META - Type for the meta property (defaults to Record<string,any>)
   */
  export interface InitialState<DATA = Record<string, any>> {
    status: "idle" | "loading" | "succeeded" | "failed";
    message: string;
    data: DATA;
    pagination?: Pagination;
    errors: Errors[];
    meta: Meta;
  }

  /**
   * Success response interface for API calls
   * @template DATA - Type for returned data (defaults to Record<string,any>)
   * @template META - Type for metadata (defaults to Record<string,any>)
   */
  export interface SuccessResponse<DATA = Record<string, any>> {
    status: "succeeded";
    message: string;
    data: DATA;
    meta: Meta;
    errors: Errors[];
  }

  /**
   * Error response interface for failed API calls
   * @template ERRORS - Type for error details (defaults to Record<string,string[]>)
   */
  export interface ErrorResponse {
    status: "failed";
    message: string;
    data: null;
    meta: Meta;
    errors: Errors[];
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
