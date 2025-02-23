import { store } from "store/store";
import { SignoutCredentials } from "services/authServices";
import { resetSignoutState } from "./signoutSlice";
import { signoutAction } from "./signoutAction";

/**
 * Dispatch a reset sign out state
 *
 * @returns void
 */
export const resetSignoutUser = (): void => {
  store.dispatch(resetSignoutState());
};


/**
 * Dispatches a user action with the provided credentials
 *
 * @param credentials - Sign out credentials object
 * @returns void
 */
export const signoutUser = (
  credentials: SignoutCredentials
): void => {
  store.dispatch(signoutAction(credentials));
};
