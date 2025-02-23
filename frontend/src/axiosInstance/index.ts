/**
 * Axios instance configuration with authentication interceptors
 * Handles automatic token injection and refresh functionality
 */

import axios from 'axios';
import { store } from 'store/store';
import {
  refreshToken,
  resetSigninUser
} from 'features/auth/signin';

const axiosInstance = axios.create({
  baseURL: process.env.REACT_APP_BASE_API_URL,
  timeout: 1000,
});

// Request interceptor - adds auth token to requests if available
axiosInstance.interceptors.request.use(
  (config) => {
    const token = store.getState().signin.data.access_token;
    if (token) {
      config.headers = config.headers || {};
      config.headers['Authorization'] = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor - handles 401 errors by refreshing token
axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const request = error.config;
    if (error.response?.status === 401 && !request._retry) {
      try {
        request._retry = true;
        refreshToken();
        const token = store.getState().signin.data.access_token;
        if (!token) {
          return Promise.reject(error);
        }
        request.headers = request.headers || {};
        request.headers['Authorization'] = `Bearer ${token}`;
        return axiosInstance(request);
      } catch (refreshError) {
        resetSigninUser()
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

export default axiosInstance;
