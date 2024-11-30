import { combineReducers } from 'redux'
import authActions from 'features/auth'

const rootReducer = combineReducers({
  signin: authActions.signinReducer,
})

export type RootState = ReturnType<typeof rootReducer>
export default rootReducer
