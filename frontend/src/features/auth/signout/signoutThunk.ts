import { createAsyncThunk } from "@reduxjs/toolkit";
import API from 'API';
import {
  SignoutSuccessResponse,
  SignoutErrorResponse
} from "./signout.types";
import { CatchAxiosError } from 'FeatureTypes';
import { SignoutCredentials } from 'API/API.types';

// Sign out thunk
// This thunk is used to sign out the user by blocking the refresh token from the server
export const signoutThunk = createAsyncThunk(
  "signout/signoutThunk",
  async (credentials: SignoutCredentials, thunkAPI) => {
    try {
      const response = await API.signoutApi(credentials);
      return response.data as SignoutSuccessResponse;
    } catch (err: unknown) {
      const error = err as CatchAxiosError;
      let errorResponse: SignoutErrorResponse;
      if (error.response) {
        errorResponse = error.response.data;
      } else {
        errorResponse = {
          status: "failed",
          message: error.message ?? "An unknown error occurred",
          errors: {
            non_field_errors: [error.message ?? "An unknown error occurred"],
          },
        };
      }
      return thunkAPI.rejectWithValue(errorResponse);
    }
  }
);