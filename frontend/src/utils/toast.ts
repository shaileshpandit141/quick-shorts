import { nanoid } from "@reduxjs/toolkit";
import { AppDispatch } from "store/store";
import { addToast } from "features/toast";

/**
 * Triggers a toast notification with the specified parameters
 * @param dispatch - Redux dispatch function
 * @param type - Type of toast: 'success', 'error', 'info', or 'warning'
 * @param message - Message to display in the toast
 * @param duration - Optional duration in milliseconds before toast auto-dismisses
 */
export const triggerToast = (
  dispatch: AppDispatch,
  type: "success" | "error" | "info" | "warning",
  message: string,
  duration?: number
) => {
  const id = nanoid();
  dispatch(
    addToast({
      id,
      type,
      message,
      duration,
    })
  );
};
