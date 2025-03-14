import { createAsyncThunk } from "@reduxjs/toolkit";
import {
  authServices,
  VerifyUserAccountCredentials,
} from "services/authServices";
import {
  VerifyUserAccountSuccessResponse,
  VerifyUserAccountErrorResponse,
} from "./verifyUserAccount.types";
import { formatCatchAxiosError } from "utils/formatCatchAxiosError";
import { CatchAxiosError } from "BaseAPITypes";

/**
 * Redux thunk to handle user verifyUserAccount process
 *
 * @param credentials - User verifyUserAccount credentials (token)
 * @returns VerifyUserAccountSuccessResponse on successful verifyUserAccount
 * @throws verifyUserAccountErrorResponse on verifyUserAccount failure
 */
export const verifyUserAccountAction = createAsyncThunk<
  VerifyUserAccountSuccessResponse,
  VerifyUserAccountCredentials,
  { rejectValue: VerifyUserAccountErrorResponse }
>(
  "verifyUserAccount/verifyUserAccountAction",
  async (credentials: VerifyUserAccountCredentials, thunkAPI) => {
    try {
      // Call verifyUserAccount API endpoint
      const response = await authServices.verifyUserAccount(credentials);
      return response.data as VerifyUserAccountSuccessResponse;
    } catch (err: unknown) {
      const error = err as CatchAxiosError;
      let errorResponse = formatCatchAxiosError(error);
      return thunkAPI.rejectWithValue(errorResponse);
    }
  }
);
