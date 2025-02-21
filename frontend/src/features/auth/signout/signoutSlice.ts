import { createSlice } from "@reduxjs/toolkit";
import { SignoutInitialState } from "./signout.types";
import { ErrorResponse } from "FeatureTypes";
import { signoutAction } from './signoutAction'

/**
 * Initial state for signout slice
 */
const signoutIntitlState: SignoutInitialState = {
  status: 'idle',
  message: '',
  data: null,
  errors: [],
  meta: {
    request_id: "",
    timestamp: "",
    response_time: '',
    documentation_url: "",
    rate_limit: []
  }
}

/**
 * Redux slice containing signout state logic and reducers
 */
const signoutSlice = createSlice({
  name: "signout",
  initialState: signoutIntitlState,
  reducers: {
    // Reset signout state to initial values
    resetSignoutState: (state) => {
      Object.assign(state, signoutIntitlState);
    },
  },
  extraReducers: (builder) => {
    builder
      // Handle signout async states
      .addCase(signoutAction.pending, (state) => {
        state.status = "loading";
      })
      .addCase(signoutAction.fulfilled, (state, action) => {
        Object.assign(state, action.payload);
      })
      .addCase(signoutAction.rejected, (state, action) => {
        Object.assign(state, action.payload as ErrorResponse);
      });
  },
});

// Export signout slice actions
export const {
  reducer: signoutReducer,
  actions: { resetSignoutState }
} = signoutSlice
