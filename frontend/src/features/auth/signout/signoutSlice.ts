/*
 * Redux slice for managing signout state and operations
  * @module signoutSlice
 */

import { createSlice } from "@reduxjs/toolkit";
import {
  SignoutInitialState,
  SignoutErrorResponse
} from "./signout.types";
import {
  signoutThunk
} from './signoutThunk'

/**
 * Initial state for signout slice
 * Contains status, message, data, errors and meta information
 */

const signoutIntitlState: SignoutInitialState = {
  status: 'idle',
  message: '',
  data: null,
  errors: null,
  meta: null
}

/**
 * Redux slice containing signout state logic and reducers
 */

const signoutSlice = createSlice({
  name: 'signout',
  initialState: signoutIntitlState,
  reducers: {
    // Reset signout state to initial values
    resetSignoutState: (state) => {
      state.status = 'idle'
      state.message = ''
      state.data = null
      state.errors = null
      state.meta = null
    }
  },
  extraReducers: (builder) => {
    builder
      // Handle signout async states
      .addCase(signoutThunk.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(signoutThunk.fulfilled, (state, action) => {
        const { status, message, data, meta } = action.payload
        state.status = status
        state.message = message
        state.data = data
        state.meta = meta
      })
      .addCase(signoutThunk.rejected, (state, action) => {
        const { status, message, errors } = action.payload as SignoutErrorResponse
        state.status = status
        state.message = message
        state.errors = errors
      })
  }
})

// Export signout slice actions
const signoutReducer = signoutSlice.reducer
export default signoutReducer
export const { resetSignoutState } = signoutSlice.actions
