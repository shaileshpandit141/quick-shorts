import { refreshTokenThunk, signinThunk } from "./signin/signinThunk";
import signinReducer, { resetSigninState } from "./signin/signinSlice";
import { useSigninSelector } from "./signin/signinSelector";
import { signupThunk } from "./signup/signupThunk";
import signupReducer, { resetSignupState } from "./signup/signupSlice";
import { useSignupSelector } from "./signup/signupSelector";
import { signoutThunk } from "./signout/signoutThunk";
import signoutReducer, { resetSignoutState } from "./signout/signoutSlice";
import { useSignoutSelector } from "./signout/signoutSelector";

// Export all the features from auth
export {
  refreshTokenThunk,
  resetSigninState,
  signinReducer,
  signinThunk,
  useSigninSelector,
  resetSignupState,
  signupReducer,
  signupThunk,
  useSignupSelector,
  resetSignoutState,
  signoutReducer,
  signoutThunk,
  useSignoutSelector,
};