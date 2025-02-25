import { configureStore } from "@reduxjs/toolkit";
import { RootState } from "./rootReducer";
import rootReducer from "./rootReducer";

const store = configureStore<RootState>({
  reducer: rootReducer,
});

export type AppDispatch = typeof store.dispatch;
export { store };
