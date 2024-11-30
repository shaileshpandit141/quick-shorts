// Imports
import { createSlice } from "@reduxjs/toolkit"
import { ErrorResponse } from "ErrorResponse.d"
import { SigninIntitlState } from "./signin.types"
import { signinThunk, refreshTokenThunk } from './signinThunk'

// Initial state
const signinIntitlState: SigninIntitlState = {
  status: 'idle',
  message: '',
  data: null,
  error: null,
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
      state.data = null
      state.error = null
      state.meta = null
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
      })
      .addCase(signinThunk.rejected, (state, action) => {
        const { status, message, error } = action.payload as ErrorResponse
        state.status = status
        state.message = message
        state.error = error
      })

      // Refresh token cases
      .addCase(refreshTokenThunk.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(refreshTokenThunk.fulfilled, (state, action) => {
        const { status, message, data, meta } = action.payload
        state.status = status
        state.message = message
        if (state.data) {
          state.data.access_token = data.access_token
        }
        state.meta = meta
      })
      .addCase(refreshTokenThunk.rejected, (state, action) => {
        const { status, message, error } = action.payload as ErrorResponse
        state.status = status
        state.message = message
        state.error = error
      })
  }
})

const signinReducer = signinSlice.reducer;
export default signinReducer;
export const { resetSigninState } = signinSlice.actions
