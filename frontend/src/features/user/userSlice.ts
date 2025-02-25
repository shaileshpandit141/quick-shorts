import { createSlice } from "@reduxjs/toolkit";
import { UserInitialState } from "./user.types";
import { userAction } from "./userAction";

/**
 * # Initial state for user slice
 * Contains status, message, data, errors and meta information
 */
const userInitialState: UserInitialState = {
  status: "idle",
  message: "",
  data: null,
  errors: [],
  meta: {
    request_id: "",
    timestamp: "",
    response_time: "",
    documentation_url: "",
    rate_limit: [],
  },
};

/**
 * Redux slice containing user state logic and reducers
 */
const userSlice = createSlice({
  name: "user",
  initialState: userInitialState,
  reducers: {
    resetUserState: (state) => {
      Object.assign(state, userInitialState);
    },
  },
  extraReducers: (builder) => {
    builder
      // Handle user async states
      .addCase(userAction.pending, (state) => {
        state.status = "loading";
      })
      .addCase(userAction.fulfilled, (state, action) => {
        Object.assign(state, action.payload);
      })
      .addCase(userAction.rejected, (state, action) => {
        Object.assign(state, action.payload);
      });
  },
});

// Export user slice actions
export const {
  reducer: userReducer,
  actions: { resetUserState },
} = userSlice;
