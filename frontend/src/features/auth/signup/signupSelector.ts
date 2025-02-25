import { useSelector } from "react-redux";
import { SignupInitialState } from "./signup.types";

/**
 * Custom hook to select signup state from Redux store
 * @returns {SignupInitialState} Current signup state
 */
export const useSignupUserSelector = (): SignupInitialState => {
  return useSelector((state: { signup: SignupInitialState }) => state.signup);
};
