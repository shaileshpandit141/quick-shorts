import { axiosInstance } from "axiosInstance";
import { getBaseAPIURL } from "utils";

/**
 * APIs using custom Axios instance
 * Currently empty, reserved for future use
 */
export const userServices = {
  /** Signs out authenticated user */
  fetchUser: () => {
    return axiosInstance.get(`${getBaseAPIURL()}/api/v1/auth/user/`);
  },
};
