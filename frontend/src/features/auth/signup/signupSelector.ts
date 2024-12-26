import { useSelector } from "react-redux";
import { SignupInitialState } from "./signup.types";

export const useSignupSelector = () => {
  return useSelector((state: {signup: SignupInitialState}) => state.signup)
}