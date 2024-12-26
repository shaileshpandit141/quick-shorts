import { createAsyncThunk } from "@reduxjs/toolkit";
import API from 'API';
import {
  SignupSuccessResponse,
  SignupErrorResponse
} from "./signup.types";
import { SignupCredentials } from 'API/API.types';
import { CatchAxiosError } from 'FeatureTypes';

// Sign up thunk
export const signupThunk = createAsyncThunk(
  "signup/signupThunk",
  async (credentials: SignupCredentials, thunkAPI) => {
    try {
      const response = await API.signupApi(credentials);
      return response.data as SignupSuccessResponse;
    } catch (err: unknown) {
      const error = err as CatchAxiosError;
      let errorResponse: SignupErrorResponse;
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