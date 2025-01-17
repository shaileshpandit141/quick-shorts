/**
 * Types and interfaces for handling user signout functionality
 */
import {
  InitialState,
  SuccessResponse
} from "FeatureTypes";

/** Initial state interface for signout feature */
export interface SignoutInitialState extends InitialState<
  { detail: string } | null
> { }

/** Success response interface for signout */
export interface SignoutSuccessResponse extends SuccessResponse<
  { detail: string }
> { }
