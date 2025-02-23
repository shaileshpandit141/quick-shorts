/**
 * Redux slice for managing toast notifications
 * @module toastSlice
 */

import { createSlice, PayloadAction } from "@reduxjs/toolkit";
import { Toast, ToastState } from "./toast.types";

// Initial state with empty toasts array
const initialState: ToastState = {
  toasts: []
};

const toastSlice = createSlice({
  name: "toast",
  initialState,
  reducers: {
    // Rest toast notification to state
    resetToastState: (state) => {
      Object.assign(state, initialState);
    },
    // Add new toast notification to state
    addToast: (state, action: PayloadAction<Toast>) => {
      state.toasts.push(action.payload);
    },
    // Remove toast notification by ID
    removeToast: (state, action: PayloadAction<string>) => {
      state.toasts = state.toasts.filter(
        (toast) => toast.id !== action.payload
      );
    },
  },
});

export const {
  reducer: toastReducer,
  actions: { addToast, removeToast, resetToastState },
} = toastSlice;
