import { store } from "store/store";
import { userAction } from "./userAction";
import { resetUserState } from "./userSlice";

/**
 * Dispatch a user action
 *
 * @returns void
 */
export const dispatchUserAction = (): void => {
  store.dispatch(userAction());
};



/**
 * Reset user state
 *
 * @returns void
 */
export const dispatchResetUserState = (): void => {
  store.dispatch(resetUserState());
};
