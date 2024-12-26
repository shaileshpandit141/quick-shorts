import { combineReducers } from 'redux'
import { signinReducer, signupReducer } from 'features/auth'

const rootReducer = combineReducers({
  signin: signinReducer,
  signup: signupReducer
})

export type RootState = ReturnType<typeof rootReducer>
export default rootReducer
