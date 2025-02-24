import axios from "axios";
import { getBaseAPIURL } from "utils";
import {
  SigninCredentials,
  SignupCredentials,
  GoogleSigninCredentials,
  SignoutCredentials,
  RefreshTokenCredentials,
  VerifyUserAccountCredentials,
} from "./authServices.types";

/** Base API URL from environment variables */
const BASE_API_URL = getBaseAPIURL();

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

  googleSignin: (credentials: GoogleSigninCredentials) => {
    return axios.post(
      `${BASE_API_URL}/api/v1/auth/google/callback/`,
      credentials
    );
  },

  /** Refreshes authentication token */
  refreshToken: (credentials: RefreshTokenCredentials) => {
    return axios.post(
      `${BASE_API_URL}/api/v1/auth/signin/token/refresh/`,
      credentials
    );
  },

  /** Sign out authenticated user */
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
