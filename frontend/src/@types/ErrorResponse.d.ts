declare module 'ErrorResponse.d' {
  export interface ErrorResponse {
    status: 'failed';
    message: string;
    error: {
      [key: string]: string[];
    };
  }

  export interface CatchErrorResponse {
    response?: {
      data: ErrorResponse
    }
    message?: ErrorResponse
  }

}
