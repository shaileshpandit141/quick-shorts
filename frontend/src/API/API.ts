import axios from 'axios'
// import axiosInstance from 'axiosInstance';
import {
  SigninCredentials,
  RefreshTokenCredentials,
  SignoutCredentials,
  SignupCredentials
} from './API.types';

const BASE_API_URL = process.env.REACT_APP_BASE_API_URL

const AxiosAPIs = {
  signupApi: (credentials: SignupCredentials) => {
    return axios.post(`${BASE_API_URL}/api/v1/auth/signup/`, credentials)
  },
  signinApi: (credentials: SigninCredentials) => {
    return axios.post(`${BASE_API_URL}/api/v1/auth/signin/token/`, credentials)
  },
  refreshTokenApi: (credentials: RefreshTokenCredentials) => {
    return axios.post(`${BASE_API_URL}/api/v1/auth/signin/token/refresh/`, credentials)
  },
  signoutApi: (credentials: SignoutCredentials) => {
    return axios.post(`${BASE_API_URL}/api/v1/auth/signout/`, credentials)
  },
}

const AxiosInstanceAPIs = {

}

const APIs = { ...AxiosAPIs, ...AxiosInstanceAPIs }
export default APIs
