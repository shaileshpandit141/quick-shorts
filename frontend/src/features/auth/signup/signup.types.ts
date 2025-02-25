// Import necessary types from FeatureTypes
import { InitialState, SuccessResponse } from "FeatureTypes";

/**
 * Interface for signup initial state
 */
export interface SignupInitialState
  extends InitialState<{ detail: string } | null> {}

/**
 * Interface for successful signup response
 */
export interface SignupSuccessResponse
  extends SuccessResponse<{ detail: string }> {}
