import { createAsyncThunk } from "@reduxjs/toolkit";
import { userServices } from "services/userServices";
import { UserSuccessResponse, UserErrorResponse } from "./user.types";
import { CatchAxiosError } from "BaseAPITypes";
import { formatCatchAxiosError } from "utils/formatCatchAxiosError";

/**
 * Redux thunk action creator for user authentication
 * Makes an API call to authenticate user with provided credentials
 * Returns user data on success or formatted error on failure
 *
 * @param credentials - User login credentials (email/password)
 * @param thunkAPI - Redux toolkit thunk API object
 * @returns UserSuccessResponse on success, formatted error message on failure
 */
export const userAction = createAsyncThunk<
  UserSuccessResponse,
  void,
  { rejectValue: UserErrorResponse }
>("user/userAction", async (_, thunkAPI) => {
  try {
    const response = await userServices.fetchUser();
    return response.data as UserSuccessResponse;
  } catch (err: unknown) {
    const error = err as CatchAxiosError;
    return thunkAPI.rejectWithValue(formatCatchAxiosError(error));
  }
});
