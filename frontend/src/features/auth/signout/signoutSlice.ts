/*
 * Redux slice for managing signout state and operations
  * @module signoutSlice
 */

import { createSlice } from "@reduxjs/toolkit";
import { SignoutInitialState } from "./signout.types";
import { ErrorResponse } from "FeatureTypes";
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
  errors: [],
  meta: {
    request_id: "",
    timestamp: "",
    documentation_url: "",
    rate_limit: []
  }
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
    }
  },
  extraReducers: (builder) => {
    builder
      // Handle signout async states
      .addCase(signoutThunk.pending, (state) => {
        state.status = 'loading'
      })
      .addCase(signoutThunk.fulfilled, (state, action) => {
        Object.assign(state, action.payload)
      })
      .addCase(signoutThunk.rejected, (state, action) => {
        Object.assign(state, action.payload as ErrorResponse)
      })
  }
})

// Export signout slice actions
export const {
  reducer: signoutReducer,
  actions: { resetSignoutState }
} = signoutSlice
