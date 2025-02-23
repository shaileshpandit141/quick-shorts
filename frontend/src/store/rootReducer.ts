/**
 * Root reducer configuration that combines all feature reducers
 */
import { combineReducers } from "redux";
import { signinReducer } from "features/auth/signin";
import { signoutReducer } from "features/auth/signout";
import { signupReducer } from "features/auth/signup";
import { verifyUserAccountReducer } from "features/auth/verifyUserAccount";
import { userReducer } from "features/user";
import { toastReducer } from "features/toast";

const rootReducer = combineReducers({
  signin: signinReducer,
  signout: signoutReducer,
  signup: signupReducer,
  verifyUserAccount: verifyUserAccountReducer,
  toast: toastReducer,
  user: userReducer,
});

// Type definition for the complete app state
export type RootState = ReturnType<typeof rootReducer>;
export default rootReducer;
