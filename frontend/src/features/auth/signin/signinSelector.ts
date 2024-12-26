import { useSelector } from "react-redux";
import { SigninInitialState } from "./signin.types";

export const useSigninSelector = () => {
  return useSelector((state: {signin: SigninInitialState}) => state.signin)
}
