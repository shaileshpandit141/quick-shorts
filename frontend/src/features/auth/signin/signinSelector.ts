import { useSelector } from "react-redux";
import { SigninIntitlState } from "./signin.types";

export const useSigninSelector = () => {
  return useSelector((state: {signin: SigninIntitlState}) => state.signin)
}
