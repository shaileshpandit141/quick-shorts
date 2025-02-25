import { InitialState, SuccessResponse } from "FeatureTypes";

// Interface for initial sign-in state
export interface SigninInitialState
  extends InitialState<{
    access_token: string | null;
    refresh_token: string | null;
  }> {}

// Interface for successful sign-in response
export interface SigninSuccessResponse
  extends SuccessResponse<{
    access_token: string;
    refresh_token: string;
  }> {}

// Interface for successful token refresh response
export interface RefreshTokenSuccessResponse
  extends SuccessResponse<{
    access_token: string;
  }> {}
