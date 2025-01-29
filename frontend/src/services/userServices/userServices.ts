import axios from 'axios'
import axiosInstance from 'axiosInstance';
import { get_absolute_url } from 'utils';

/** Base API URL from environment variables */
const BASE_API_URL = get_absolute_url(null)

/**
 * APIs using custom Axios instance
 * Currently empty, reserved for future use
 */
export const userServices = {
  /** Signs out authenticated user */
  fetchUser: () => {
    return axiosInstance.get(`${BASE_API_URL}/api/v1/auth/user/`)
  },
}
