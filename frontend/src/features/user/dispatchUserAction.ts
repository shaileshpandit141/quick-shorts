import { store } from "store/store";
import { userAction } from "./userAction";

/**
 * Dispatch a user action
 *
 * @returns void
 */
export const dispatchUserAction = (): void => {
  store.dispatch(userAction());
};
