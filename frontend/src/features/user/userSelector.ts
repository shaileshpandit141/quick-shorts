import { useSelector } from "react-redux";
import { UserInitialState } from "./user.types";

/**
 * Custom hook to select user state from Redux store
 * @returns {UserInitialState} Current user state
 */
export const useUserSelector = (): UserInitialState => {
  return useSelector((state: { user: UserInitialState }) => (
    state.user
  ))
}
