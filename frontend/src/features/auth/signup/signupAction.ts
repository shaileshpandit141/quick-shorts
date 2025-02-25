import { createAsyncThunk } from "@reduxjs/toolkit";
import { authServices, SignupCredentials } from "services/authServices";
import { SignupSuccessResponse } from "./signup.types";
import { formatCatchAxiosError } from "utils/formatCatchAxiosError";
import { CatchAxiosError, ErrorResponse } from "FeatureTypes";

/**
 * Redux thunk to handle user signup process
 *
 * @param credentials - User signup credentials (email, password, etc)
 * @returns SignupSuccessResponse on successful signup
 * @throws SignupErrorResponse on signup failure
 */
export const signupAction = createAsyncThunk<
  SignupSuccessResponse,
  SignupCredentials,
  { rejectValue: ErrorResponse }
>("signup/signupAction", async (credentials: SignupCredentials, thunkAPI) => {
  try {
    // Call signup API endpoint
    const response = await authServices.signup(credentials);
    return response.data as SignupSuccessResponse;
  } catch (err: unknown) {
    const error = err as CatchAxiosError;
    let errorResponse = formatCatchAxiosError(error);
    return thunkAPI.rejectWithValue(errorResponse);
  }
});
