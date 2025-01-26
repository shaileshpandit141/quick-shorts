import { AppDispatch } from "store/store";
import { userAction } from "./userAction";

/**
 * Dispatches a user action with the provided credentials
 *
 * @param dispatch - Redux dispatch function
 * @param credentials - User credentials object containing login info
 * @returns void
 */
export const dispatchUserAction = (dispatch: AppDispatch): void => {
  dispatch(userAction());
};
