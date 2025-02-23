import { useSelector } from "react-redux";
import { VerifyUserAccountInitialState } from "./verifyUserAccount.types";

/**
 * Custom hook to select veryfy user account state from Redux store
 * @returns {VerifyUserAccountInitialState} Current veryfy user account state
 */
export const useVerifyUserAccountSelector =
  (): VerifyUserAccountInitialState => {
    return useSelector(
      (state: { verifyUserAccount: VerifyUserAccountInitialState }) =>
        state.verifyUserAccount
    );
  };
