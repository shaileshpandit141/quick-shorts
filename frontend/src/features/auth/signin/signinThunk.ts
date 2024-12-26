import { createAsyncThunk } from '@reduxjs/toolkit'
import API from 'API'
import {
  SigninInitialState,
  SigninSuccessResponse,
  RefreshTokenSuccessResponse,
  SigninErrorResponse,
  RefreshTokenErrorResponse
} from './signin.types'
import { SigninCredentials } from 'API/API.types'
import { CatchAxiosError } from 'FeatureTypes'

// Sign in thunk
export const signinThunk = createAsyncThunk(
  'signin/signinThunk',
  async (credentials: SigninCredentials, thunkAPI) => {
    try {
      const response = await API.signinApi(credentials)
      return response.data as SigninSuccessResponse
    } catch (err: unknown) {
      const error = err as CatchAxiosError
      let errorResponse: SigninErrorResponse
      if (error.response) {
        errorResponse = error.response.data
      } else {
        errorResponse = {
          status: 'failed',
          message: error.message ?? 'An unknown error occurred',
          errors: {
            non_field_errors: [error.message ?? 'An unknown error occurred']
          }
        }
      }
      return thunkAPI.rejectWithValue(errorResponse)
    }
  }
)

// Refresh token thunk
export const refreshTokenThunk = createAsyncThunk(
  'signin/refreshTokenThunk',
  async (_: void, thunkAPI) => {
    const state = thunkAPI.getState() as SigninInitialState
    const refresh_token = state.data?.refresh_token

    if (!refresh_token) {
      return thunkAPI.rejectWithValue({
        status: 'failed',
        message: 'No refresh token available',
        errors: {
          non_field_errors: ['No refresh token available']
        }
      })
    }

    try {
      const response = await API.refreshTokenApi({
        refresh_token: refresh_token
      })
      return response.data as RefreshTokenSuccessResponse
    } catch (err: unknown) {
      const error = err as CatchAxiosError
      let errorResponse: RefreshTokenErrorResponse
      if (error.response) {
        errorResponse = error.response.data
      } else {
        errorResponse = {
          status: 'failed',
          message: error.message ?? 'An unknown error occurred',
          errors: {
            non_field_errors: [error.message ?? 'An unknown error occurred']
          }
        }
      }
      return thunkAPI.rejectWithValue(errorResponse)
    }
  }
)
