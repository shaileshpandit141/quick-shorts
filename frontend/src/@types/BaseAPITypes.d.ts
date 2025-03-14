export declare module "BaseAPITypes" {
  /**
   * API Meta Information
   */
  export interface Meta {
    request_id: string;
    timestamp: string;
    response_time: string;
    documentation_url: string;
    rate_limits: {
      throttled_by: string | null;
      throttles: {
        [key: string]: ThrottleInfo;
      };
    };
  }

  export interface ThrottleInfo {
    limit: number;
    remaining: number;
    reset_time: string;
    retry_after: string;
  }

  /**
   * General Error Structure
   */
  export interface Errors {
    detail?: string;
    non_field_errors?: string[];
    [key: string]: string[] | string | undefined;
  }

  /**
   * Base state structure for Redux slices
   */
  export interface BaseState {
    status: "idle" | "loading" | "succeeded" | "failed";
    status_code: number | null;
    message: string;
    meta: Meta | {};
  }

  /**
   * Generic state structure for Redux slices
   * Supports both `{}` and `[]` responses in `data`
   */
  export interface InitialState<
    DATA = Record<string, any> | Record<string, any>[],
    ERRORS,
  > extends BaseState {
    data: DATA;
    errors: Errors & ERRORS;
  }

  /**
   * State structure for paginated API responses
   */
  export interface PaginatedInitialState<
    DATA = Record<string, any>,
    ERRORS = Errors,
  > extends BaseState {
    data:
      | {
          current_page: number;
          total_pages: number;
          total_items: number;
          items_per_page: number;
          has_next: boolean;
          has_previous: boolean;
          next_page_number: number | null;
          previous_page_number: number | null;
          next: string | null;
          previous: string | null;
          results: DATA[];
        }
      | {};
    errors: ERRORS;
  }

  /**
   * Success response interface for API calls
   */
  export interface SuccessResponse<DATA = Record<string, any>>
    extends BaseState {
    status: "succeeded";
    data: DATA;
    errors: {};
  }

  /**
   * Error response interface for failed API calls
   */
  export interface ErrorResponse<ERRORS = Errors> extends BaseState {
    status: "failed";
    data: {};
    errors: Errors & ERRORS;
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
