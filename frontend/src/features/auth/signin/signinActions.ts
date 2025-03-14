import { store } from "store/store";
import { createAsyncThunk } from "@reduxjs/toolkit";
import {
  authServices,
  SigninCredentials,
  GoogleSigninCredentials,
} from "services/authServices";
import {
  SigninSuccessResponse,
  SigninErrorResponse,
  RefreshTokenSuccessResponse,
  RefreshTokenErrorResponse
} from "./signin.types";
import { CatchAxiosError } from "BaseAPITypes";
import { formatCatchAxiosError } from "utils/formatCatchAxiosError";

/**
 * Redux thunk to handle user sign in
 * Makes API call with credentials and returns success/error response
 */
export const signinAction = createAsyncThunk<
  SigninSuccessResponse,
  SigninCredentials,
  { rejectValue: SigninErrorResponse }
>("signin/signinAction", async (credentials: SigninCredentials, thunkAPI) => {
  try {
    const response = await authServices.signin(credentials);
    return response.data as SigninSuccessResponse;
  } catch (err: unknown) {
    const error = err as CatchAxiosError;
    let errorResponse = formatCatchAxiosError(error);
    return thunkAPI.rejectWithValue(errorResponse);
  }
});

// Redux thunk to handle user google Signin process
export const googleSigninAction = createAsyncThunk<
  SigninSuccessResponse,
  GoogleSigninCredentials,
  { rejectValue: SigninErrorResponse }
>(
  "signin/googleSigninAction",
  async (credentials: GoogleSigninCredentials, thunkAPI) => {
    try {
      const response = await authServices.googleSignin(credentials);
      return response.data as SigninSuccessResponse;
    } catch (err: unknown) {
      const error = err as CatchAxiosError;
      let errorResponse = formatCatchAxiosError(error);
      return thunkAPI.rejectWithValue(errorResponse);
    }
  }
);

/**
 * Redux thunk to refresh authentication token
 * Gets refresh token from state and requests new access token
 * Returns error if no refresh token exists
 */
export const refreshTokenAction = createAsyncThunk<
  RefreshTokenSuccessResponse,
  void,
  { rejectValue: RefreshTokenErrorResponse }
>("signin/refreshTokenAction", async (_, thunkAPI) => {
  const refresh_token = store.getState().signin.data?.refresh_token;
  try {
    const response = await authServices.refreshToken({
      refresh_token: refresh_token || "",
    });
    return response.data as RefreshTokenSuccessResponse;
  } catch (err: unknown) {
    const error = err as CatchAxiosError;
    let errorResponse = formatCatchAxiosError(error);
    return thunkAPI.rejectWithValue(errorResponse);
  }
});
