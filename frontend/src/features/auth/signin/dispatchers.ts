import { store } from "store";
import {
  signinAction,
  refreshTokenAction,
  googleSigninAction,
} from "./signinActions";
import { resetSigninState } from "./signinSlice";
import {
  SigninCredentials,
  GoogleSigninCredentials,
} from "services/authServices";

// Dispatch a refresh token action
export const refreshToken = (): void => {
  store.dispatch(refreshTokenAction());
};

// Dispatch a reset sign in state
export const resetSigninUser = (): void => {
  store.dispatch(resetSigninState());
};

// Dispatch a user action with the provided credentials
export const signinUser = (credentials: SigninCredentials): void => {
  store.dispatch(signinAction(credentials));
};

// Dispatch a Google Sign in action with the provided credentials
export const googleSigninUser = (
  credentials: GoogleSigninCredentials,
): void => {
  store.dispatch(googleSigninAction(credentials));
};
