import { store } from "store";
import { signinAction, refreshTokenAction } from "./signinAction";
import { resetSigninState } from './signinSlice'
import { SigninCredentials } from "services/authServices";

/**
 * Dispatch a refresh token action
 *
 * @returns void
 */
export const refreshToken = (): void => {
  store.dispatch(refreshTokenAction())
};

/**
 * Dispatch a reset sign in state
 *
 * @returns void
 */
export const resetSigninUser = (): void => {
  store.dispatch(resetSigninState())
};

/**
 * Dispatch a user action with the provided credentials
 *
 * @param credentials - Sign in credentials object
 * @returns void
 */
export const signinUser = (
  credentials: SigninCredentials
): void => {
  store.dispatch(signinAction(credentials))
};
