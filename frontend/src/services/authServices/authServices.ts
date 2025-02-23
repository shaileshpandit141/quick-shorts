import axios from "axios";
import { get_absolute_url } from "utils";
import {
  SigninCredentials,
  SignupCredentials,
  SignoutCredentials,
  RefreshTokenCredentials,
  VerifyUserAccountCredentials,
} from "./authServices.types";

/** Base API URL from environment variables */
const BASE_API_URL = get_absolute_url(null);

/**
 * APIs using direct Axios instance
 */
export const authServices = {
  /** Creates new user account */
  signup: (credentials: SignupCredentials) => {
    return axios.post(`${BASE_API_URL}/api/v1/auth/signup/`, credentials);
  },
  /** Authenticates existing user */
  signin: (credentials: SigninCredentials) => {
    return axios.post(`${BASE_API_URL}/api/v1/auth/signin/token/`, credentials);
  },
  /** Refreshes authentication token */
  refreshToken: (credentials: RefreshTokenCredentials) => {
    return axios.post(
      `${BASE_API_URL}/api/v1/auth/signin/token/refresh/`,
      credentials
    );
  },
  /** Signs out authenticated user */
  signout: (credentials: SignoutCredentials) => {
    return axios.post(`${BASE_API_URL}/api/v1/auth/signout/`, credentials);
  },
  /** Verifies user account */
  verifyUserAccount: (credentials: VerifyUserAccountCredentials) => {
    return axios.post(
      `${BASE_API_URL}/api/v1/auth/verify-user-account/confirm/`,
      credentials
    );
  },
};
