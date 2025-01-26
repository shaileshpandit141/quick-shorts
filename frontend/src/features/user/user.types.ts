import { InitialState, SuccessResponse } from 'FeatureTypes';

/**
 * Interface representing core user data fields
 * Contains basic user information and authentication status
 */
interface UserData {
  id: number;
  email: string;
  username: string;
  first_name: string;
  last_name: string;
  avatar: string;
  is_verified: boolean;
  is_staff: boolean;
  is_superuser: boolean;
}

/**
 * Interface extending InitialState to handle UserData
 * Used for managing user state with nullable UserData
 */
export interface UserInitialState extends InitialState<
  UserData | null
> { }

/**
 * Interface extending SuccessResponse for UserData
 * Used for handling successful user data API responses
 */
export interface UserSuccessResponse extends SuccessResponse<
  UserData
> { }
