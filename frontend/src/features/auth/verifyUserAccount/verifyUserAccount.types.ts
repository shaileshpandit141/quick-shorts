// Import necessary types from FeatureTypes
import { InitialState, SuccessResponse } from "FeatureTypes";

/**
 * Interface for Verify User Account initial state
 */
export interface VerifyUserAccountInitialState
  extends InitialState<{ detail: string } | null> {}

/**
 * Interface for successful Verify User Account response
 */
export interface VerifyUserAccountSuccessResponse
  extends SuccessResponse<{ detail: string }> {}
