import { createAsyncThunk } from '@reduxjs/toolkit'
import API from 'API'
import {
  SigninInitialState,
  SigninSuccessResponse,
  RefreshTokenSuccessResponse
} from './signin.types'
import { SigninCredentials } from 'API/API.types'
import { CatchAxiosError, ErrorResponse } from 'FeatureTypes'
import { formatCatchAxiosError } from 'utils/formatCatchAxiosError'

/**
 * Redux thunk to handle user sign in
 * Makes API call with credentials and returns success/error response
 */
export const signinThunk = createAsyncThunk<
  SigninSuccessResponse,
  SigninCredentials,
  { rejectValue: ErrorResponse }
>(
  'signin/signinThunk',
  async (credentials: SigninCredentials, thunkAPI) => {
    try {
      const response = await API.signinApi(credentials)
      return response.data as SigninSuccessResponse
    } catch (err: unknown) {
      const error = err as CatchAxiosError
      let errorResponse = formatCatchAxiosError(error)
      return thunkAPI.rejectWithValue(errorResponse)
    }
  }
)

/**
 * Redux thunk to refresh authentication token
 * Gets refresh token from state and requests new access token
 * Returns error if no refresh token exists
 */
export const refreshTokenThunk = createAsyncThunk(
  'signin/refreshTokenThunk',
  async (_: void, thunkAPI) => {
    const state = thunkAPI.getState() as SigninInitialState
    const refresh_token = state.data?.refresh_token
    try {
      const response = await API.refreshTokenApi({
        refresh_token: refresh_token || ""
      })
      return response.data as RefreshTokenSuccessResponse
    } catch (err: unknown) {
      const error = err as CatchAxiosError
      let errorResponse = formatCatchAxiosError(error)
      return thunkAPI.rejectWithValue(errorResponse)
    }
  }
)
