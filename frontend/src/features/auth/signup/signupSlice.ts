/**
 * Redux slice for managing signup state and operations
 * @module signupSlice
 */

import { createSlice } from "@reduxjs/toolkit";
import { SignupInitialState } from "./signup.types";
import { ErrorResponse } from "FeatureTypes";
import { signupThunk } from './signupThunk'

/**
 * Initial state for signup slice
 * Contains status, message, data, errors and meta information
 */
const signupIntitlState: SignupInitialState = {
  status: 'idle',
  message: '',
  data: null,
  errors: [],
  meta: {
    request_id: "",
    timestamp: "",
    documentation_url: "",
    rate_limit: []
  }
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
    }
  },
  extraReducers: (builder) => {
    builder
      // Handle signup async states
      .addCase(signupThunk.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(signupThunk.fulfilled, (state, action) => {
        Object.assign(state, action.payload)
      })
      .addCase(signupThunk.rejected, (state, action) => {
        Object.assign(state, action.payload as ErrorResponse)
      })
  }
})

// Extract reducer and actions
export const {
  reducer: signupReducer,
  actions: { resetSignupState }
} = signupSlice
