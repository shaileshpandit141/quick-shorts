/**
 * Custom hook to access signin state from Redux store
 * @returns {SigninInitialState} Current signin state
 */
import { useSelector } from "react-redux";
import { SigninInitialState } from "./signin.types";

export const useSigninSelector = (): SigninInitialState => {
  return useSelector((state: { signin: SigninInitialState }) => state.signin)
}
