import { store } from "store/store";
import { SignupCredentials } from "services/authServices";
import { signupAction } from './signupAction'
import { resetSignupState } from "./signupSlice";

/**
 * Dispatch a sign up action with the provided credentials
 *
 * @param credentials - Sign up credentials object
 * @returns void
 */
export const signupUser = (
  credentials: SignupCredentials
): void => {
  store.dispatch(signupAction(credentials));
};

/**
 * Dispatch a reset Sign up state
 *
 * @returns void
 */
export const resetSignupUser = (): void => {
  store.dispatch(resetSignupState());
};
