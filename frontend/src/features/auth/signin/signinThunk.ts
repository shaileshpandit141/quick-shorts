import { createAsyncThunk } from '@reduxjs/toolkit'
import API from 'API'
import { SigninCredentials } from 'APICredentials'
import { ErrorResponse, CatchErrorResponse } from 'ErrorResponse.d'
import {
  SigninIntitlState,
  SigninSuccessResponse,
  RefreshTokenSuccessResponse
} from './signin.types'

// Error handling helper
const createErrorResponse = (error: CatchErrorResponse): ErrorResponse => {
  if (error.response) {
    return error.response.data as ErrorResponse
  } else {
    return {
      status: 'failed',
      message: error.message ?? 'An unknown error occurred',
      error: {
        non_field_errors: [error.message ?? 'An unknown error occurred']
      }
    } as ErrorResponse
  }
}

// Sign in thunk
export const signinThunk = createAsyncThunk(
  'signin/signinThunk',
  async (credentials: SigninCredentials, thunkAPI) => {
    try {
      const response = await API.signinApi(credentials)
      return response.data as SigninSuccessResponse
    } catch (error: unknown) {
      const err = error as CatchErrorResponse
      const errorResponse = createErrorResponse(err)
      return thunkAPI.rejectWithValue(errorResponse)
    }
  }
)

// Refresh token thunk
export const refreshTokenThunk = createAsyncThunk(
  'signin/refreshTokenThunk',
  async (_: void, thunkAPI) => {
    const state = thunkAPI.getState() as SigninIntitlState
    const refresh_token = state.data?.refresh_token

    if (!refresh_token) {
      return thunkAPI.rejectWithValue({
        status: 'failed',
        message: 'No refresh token available',
        error: {
          non_field_errors: ['No refresh token available']
        }
      })
    }

    try {
      const response = await API.refreshAccessTokenApi({
        refresh_token: refresh_token
      })
      return response.data as RefreshTokenSuccessResponse
    } catch (error: unknown) {
      const err = error as CatchErrorResponse
      const errorResponse = createErrorResponse(err)
      return thunkAPI.rejectWithValue(errorResponse)
    }
  }
)
