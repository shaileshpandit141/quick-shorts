import { store } from "store/store";
import { VerifyUserAccountCredentials } from "services/authServices";
import { verifyUserAccountAction } from "./verifyUserAccountAction";
import { resetVerifyUserAccountState } from "./verifyUserAccountSlice";

/**
 * Dispatch a Verify User Account action with the provided credentials
 *
 * @param credentials - Verify User Account credentials object
 * @returns void
 */
export const dispatchVerifyUserAccountAction = (
  credentials: VerifyUserAccountCredentials
): void => {
  store.dispatch(verifyUserAccountAction(credentials));
};

/**
 * Dispatch a reset Verify User Account state
 *
 * @returns void
 */
export const dispatchRestVerifyUserAccountState = (): void => {
  store.dispatch(resetVerifyUserAccountState());
};
