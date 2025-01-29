/**
 * Root reducer configuration that combines all feature reducers
 * Contains auth-related reducers for signin, signout and signup functionality
 */
import { combineReducers } from 'redux'
import { signinReducer } from 'features/auth/signin'
import { signoutReducer } from 'features/auth/signout'
import { signupReducer } from 'features/auth/signup'
import { userReducer } from 'features/user'
import { toastReducer } from 'features/toast'

const rootReducer = combineReducers({
  signin: signinReducer,
  signout: signoutReducer,
  signup: signupReducer,
  toast: toastReducer,
  user: userReducer
})

// Type definition for the complete app state
export type RootState = ReturnType<typeof rootReducer>
export default rootReducer
