import { nanoid } from "@reduxjs/toolkit";
import { store } from "store/store";
import { addToast } from "features/toast";

/**
 * Triggers a toast notification with the specified parameters
 * @param type - Type of toast: 'success', 'error', 'info', or 'warning'
 * @param message - Message to display in the toast
 * @param duration - Optional duration in milliseconds before toast auto-dismisses
 */
export const triggerToast = (
  type: "success" | "error" | "info" | "warning",
  message: string,
  duration?: number,
) => {
  const id = nanoid();
  store.dispatch(
    addToast({
      id,
      type,
      message,
      duration,
    }),
  );
};
