/**
 * Redux slice for managing signup state and operations
 * @module signupSlice
 */

import { createSlice } from "@reduxjs/toolkit";
import {
  SignupInitialState,
  SignupErrorResponse
} from "./signup.types";
import {
  signupThunk
} from './signupThunk'

/**
 * Initial state for signup slice
 * Contains status, message, data, errors and meta information
 */
const signupIntitlState: SignupInitialState = {
  status: 'idle',
  message: '',
  data: null,
  errors: null,
  meta: null
}

/**
 * Redux slice containing signup state logic and reducers
 */
const signupSlice = createSlice({
  name: 'signup',
  initialState: signupIntitlState,
  reducers: {
    // Reset signup state to initial values
    resetSignupState: (state) => {
      state.status = 'idle'
      state.message = ''
      state.data = null
      state.errors = null
      state.meta = null
    }
  },
  extraReducers: (builder) => {
    builder
      // Handle signup async states
      .addCase(signupThunk.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(signupThunk.fulfilled, (state, action) => {
        const { status, message, data, meta } = action.payload
        state.status = status
        state.message = message
        state.data = data
        state.meta = meta
      })
      .addCase(signupThunk.rejected, (state, action) => {
        const { status, message, errors } = action.payload as SignupErrorResponse
        state.status = status
        state.message = message
        state.errors = errors
      })
  }
})

// Extract reducer and actions
const signupReducer = signupSlice.reducer
export default signupReducer
export const { resetSignupState } = signupSlice.actions
