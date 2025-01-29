import { createAsyncThunk } from "@reduxjs/toolkit";
import { authServices, SignoutCredentials } from 'services/authServices';
import { SignoutSuccessResponse } from "./signout.types";
import { CatchAxiosError, ErrorResponse } from 'FeatureTypes';
import { formatCatchAxiosError } from "utils/formatCatchAxiosError";

/**
 * Redux thunk for handling user signout
 * - Makes API call to block the refresh token on the server
 * - Returns success response with status on successful signout
 * - Returns error response with details on failure
 *
 * @param credentials - User signout credentials required by the API
 * @returns SignoutSuccessResponse on success, SignoutErrorResponse on failure
 */
export const signoutAction = createAsyncThunk<
  SignoutSuccessResponse,
  SignoutCredentials,
  { rejectValue: ErrorResponse }
>(
  "signout/signoutAction",
  async (credentials: SignoutCredentials, thunkAPI) => {
    try {
      const response = await authServices.signout(credentials);
      return response.data as SignoutSuccessResponse;
    } catch (err: unknown) {
      const error = err as CatchAxiosError;
      let errorResponse = formatCatchAxiosError(error)
      return thunkAPI.rejectWithValue(errorResponse);
    }
  }
);
