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
  data: {
    detail: null
  },
  errors: {
    email: undefined,
    non_field_errors: undefined,
    password: undefined,
    confirm_password: undefined
  },
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
      state.data.detail = null
      state.errors.email = undefined
      state.errors.non_field_errors = undefined
      state.errors.password = undefined
      state.errors.confirm_password = undefined
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
        state.data.detail = data.detail
        state.meta = meta
      })
      .addCase(signupThunk.rejected, (state, action) => {
        const { status, message, errors } = action.payload as SignupErrorResponse
        state.status = status
        state.message = message
        state.errors.email = errors?.email
        state.errors.non_field_errors = errors?.non_field_errors
        state.errors.password = errors?.password
        state.errors.confirm_password = errors?.confirm_password
      })
  }
})

const signupReducer = signupSlice.reducer
export const { resetSignupState } = signupSlice.actions
export default signupReducer
