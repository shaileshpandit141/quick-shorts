import axios from 'axios'
import {
  SigninCredentials,
  RefreshTokenCredentials
} from './API.types';


const BASE_API_URL = process.env.REACT_APP_BASE_API_URL

interface Credentials {
  [key: string]: any;
}

const API = {
  // Request with axios without JWT Token.
  signupApi: (credentials: Credentials) => {
    return axios.post(`${BASE_API_URL}api/auth/signup/`, credentials)
  },
  signoutApi: (credentials: Credentials) => {
    return axios.post(`${BASE_API_URL}api/auth/signout/`, credentials)
  },
  signinApi: (credentials: SigninCredentials) => {
    return axios.post(`${BASE_API_URL}api/v1/auth/signin/token/`, credentials)
  },
  refreshTokenApi: (credentials: RefreshTokenCredentials) => {
    return axios.post(`${BASE_API_URL}api/auth/signin/token/refresh/`, credentials)
  },
  verifyEmailApi: (credentials: Credentials) => {
    return axios.post(`${BASE_API_URL}api/auth/signup/verify-email/`, credentials)
  },
  resendVerificationEmailApi: (credentials: Credentials) => {
    return axios.post(`${BASE_API_URL}api/auth/signup/resend-verification-email/`, credentials)
  },
  resetPasswordApi: (credentials: Credentials) => {
    return axios.post(`${BASE_API_URL}api/auth/password/reset/`, credentials)
  },
  resetPasswordConfirmApi: (credentials: Credentials) => {
    return axios.post(`${BASE_API_URL}api/auth/password/reset/confirm/`, credentials)
  },
}

export default API
