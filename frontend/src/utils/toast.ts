import { nanoid } from "@reduxjs/toolkit";
import { AppDispatch } from "store/store";
import { addToast } from "features/toast";

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
