import { configureStore } from '@reduxjs/toolkit'
import { RootState } from './rootReducer'
import rootReducer from './rootReducer'

export const store = configureStore<RootState>({
  reducer: rootReducer
})
