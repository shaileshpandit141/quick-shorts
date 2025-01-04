import { useSelector } from "react-redux";
import { SignoutInitialState } from "./signout.types";

/**
 * Custom hook to select signout state from Redux store
 * @returns {SignoutInitialState} Current signout state
 */
export const useSignoutSelector = (): SignoutInitialState => {
  return useSelector((state: { signout: SignoutInitialState }) => state.signout)
}
