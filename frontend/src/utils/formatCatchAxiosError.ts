import { CatchAxiosError, ErrorResponse } from "FeatureTypes";

export const formatCatchAxiosError = (error: CatchAxiosError): ErrorResponse => {
  let errorResponse: ErrorResponse
  if (error.response) {
    errorResponse = error.response.data
  } else {
    errorResponse = {
      status: 'failed',
      message: error.message ?? 'An unknown error occurred',
      data: null,
      errors: [{
        field: "none",
        code: "client_errror",
        message: error.message ?? 'An unknown error occurred',
        details: null
      }],
      meta: {
        request_id: "",
        timestamp: "",
        response_time: "",
        documentation_url: "",
        rate_limit: []
      }
    }
  }
  return errorResponse
}
