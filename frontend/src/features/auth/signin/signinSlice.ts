// Imports
import { createSlice } from "@reduxjs/toolkit"
import {
  SigninInitialState,
  SigninErrorResponse,
  RefreshTokenErrorResponse
} from "./signin.types"
import {
  signinThunk,
  refreshTokenThunk
} from './signinThunk'

// Initial state
const signinIntitlState: SigninInitialState = {
  status: 'idle',
  message: '',
  data: {
    access_token: localStorage.getItem('access_token'),
    refresh_token: localStorage.getItem('refresh_token')
  },
  errors: null,
  meta: null
}

// Slice definition
const signinSlice = createSlice({
  name: 'signin',
  initialState: signinIntitlState,
  reducers: {
    resetSigninState: (state) => {
      state.status = 'idle'
      state.message = ''
      state.data.access_token = null
      state.data.refresh_token = null
      state.errors = null
      state.meta = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  },
  extraReducers: (builder) => {
    builder
      // Sign in cases
      .addCase(signinThunk.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(signinThunk.fulfilled, (state, action) => {
        const { status, message, data, meta } = action.payload
        state.status = status
        state.message = message
        state.data = data
        state.meta = meta
        if (data?.access_token) {
          localStorage.setItem("access_token", data.access_token)
        }
        if (data?.refresh_token) {
          localStorage.setItem('refresh_token', data.refresh_token)
        }
      })
      .addCase(signinThunk.rejected, (state, action) => {
        const { status, message, errors } = action.payload as SigninErrorResponse
        state.status = status
        state.message = message
        state.errors = errors
      })

      // Refresh token cases
      .addCase(refreshTokenThunk.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(refreshTokenThunk.fulfilled, (state, action) => {
        const { status, message, data, meta } = action.payload
        state.status = status
        state.message = message
        if (data?.access_token) {
          localStorage.setItem('access_token', data.access_token)
          state.data = {
            ...state.data,
            access_token: data.access_token
          }
        }
        state.meta = meta
      })
      .addCase(refreshTokenThunk.rejected, (state, action) => {
        const { status, message, errors } = action.payload as RefreshTokenErrorResponse
        state.status = status
        state.message = message
        console.error(errors)
      })
  }
})

const signinReducer = signinSlice.reducer;
export const { resetSigninState } = signinSlice.actions
export default signinReducer;
