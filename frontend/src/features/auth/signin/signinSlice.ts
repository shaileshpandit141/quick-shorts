/**
 * Redux slice for handling authentication state management
 * Manages signin process and token refresh functionality
 */

// Required imports for authentication slice
import { createSlice } from "@reduxjs/toolkit"
import {
  SigninInitialState
} from "./signin.types"
import { ErrorResponse } from 'FeatureTypes';
import {
  signinThunk,
  refreshTokenThunk
} from './signinThunk'

// Initial authentication state with tokens from localStorage
const signinIntitlState: SigninInitialState = {
  status: 'idle',
  message: '',
  data: {
    access_token: localStorage.getItem('access_token'),
    refresh_token: localStorage.getItem('refresh_token')
  },
  errors: [],
  meta: {
    request_id: "",
    timestamp: "",
    response_time: '',
    documentation_url: "",
    rate_limit: []
  }
}

// Authentication slice definition with reducers and async thunks
const signinSlice = createSlice({
  name: 'signin',
  initialState: signinIntitlState,
  reducers: {
    // Reset auth state and clear stored tokens
    resetSigninState: (state) => {
      state.status = 'idle'
      state.message = ''
      state.data.access_token = null
      state.data.refresh_token = null
      state.errors = []
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  },
  extraReducers: (builder) => {
    builder
      // Handle signin process states
      .addCase(signinThunk.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(signinThunk.fulfilled, (state, action) => {
        const { status, message, data, meta } = action.payload
        state.status = status
        state.message = message
        state.data = data
        state.meta = meta
        localStorage.setItem("access_token", data.access_token)
        localStorage.setItem('refresh_token', data.refresh_token)
      })
      .addCase(signinThunk.rejected, (state, action) => {
        const { status, message, errors } = action.payload as ErrorResponse
        state.status = status
        state.message = message
        state.errors = errors
      })

      // Handle token refresh states
      .addCase(refreshTokenThunk.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(refreshTokenThunk.fulfilled, (state, action) => {
        const { status, message, data, meta } = action.payload
        state.status = status
        state.message = message
        state.data.access_token = data.access_token
        localStorage.setItem('access_token', data.access_token)
        state.meta = meta
      })
      .addCase(refreshTokenThunk.rejected, (state, action) => {
        const { status, message, errors } = action.payload as ErrorResponse
        state.status = status
        state.message = message
        console.error(errors)
      })
  }
})

export const {
  reducer: signinReducer,
  actions: { resetSigninState }
} = signinSlice
