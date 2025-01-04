/**
 * Authentication API endpoints using Axios
 * This module provides methods for user authentication operations
 */

import axios from 'axios'
// import axiosInstance from 'axiosInstance';
import {
  SigninCredentials,
  RefreshTokenCredentials,
  SignoutCredentials,
  SignupCredentials
} from './API.types';

/** Base API URL from environment variables */
const BASE_API_URL = process.env.REACT_APP_BASE_API_URL

/**
 * APIs using direct Axios instance
 */
const AxiosAPIs = {
  /** Creates new user account */
  signupApi: (credentials: SignupCredentials) => {
    return axios.post(`${BASE_API_URL}/api/v1/auth/signup/`, credentials)
  },
  /** Authenticates existing user */
  signinApi: (credentials: SigninCredentials) => {
    return axios.post(`${BASE_API_URL}/api/v1/auth/signin/token/`, credentials)
  },
  /** Refreshes authentication token */
  refreshTokenApi: (credentials: RefreshTokenCredentials) => {
    return axios.post(`${BASE_API_URL}/api/v1/auth/signin/token/refresh/`, credentials)
  },
  /** Signs out authenticated user */
  signoutApi: (credentials: SignoutCredentials) => {
    return axios.post(`${BASE_API_URL}/api/v1/auth/signout/`, credentials)
  },
}

/**
 * APIs using custom Axios instance
 * Currently empty, reserved for future use
 */
const AxiosInstanceAPIs = {

}

const APIs = { ...AxiosAPIs, ...AxiosInstanceAPIs }
export default APIs
