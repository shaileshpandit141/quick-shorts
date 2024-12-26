import { createSlice } from "@reduxjs/toolkit";
import {
  SignupInitialState,
  SignupErrorResponse
} from "./signup.types";
import {
  signupThunk
} from './signupThunk'

// Initial state
const signupIntitlState: SignupInitialState = {
  status: 'idle',
  message: '',
  data: null,
  errors: null,
  meta: null
}

// Slice definition
const signupSlice = createSlice({
  name: 'signup',
  initialState: signupIntitlState,
  reducers: {
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
      // Sign up cases
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

const signupReducer = signupSlice.reducer
export const { resetSignupState } = signupSlice.actions
export default signupReducer
