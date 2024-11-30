import { refreshTokenThunk, signinThunk } from "./signin/signinThunk";
import signinReducer, { resetSigninState } from "./signin/signinSlice";
import { useSigninSelector } from "./signin/signinSelector";

// Create an object with all the actions/reducers
const authActions = {
  refreshTokenThunk,
  resetSigninState,
  signinReducer,
  signinThunk,
  useSigninSelector,
};

// Export the object
export default authActions;
