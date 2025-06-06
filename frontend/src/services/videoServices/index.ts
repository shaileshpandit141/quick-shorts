import { axiosInstance } from "axiosInstance";
import { getBaseAPIURL } from "utils/getBaseAPIURL";
import { VideoCredentials } from "./videoServices.types";

const baseAPIURL = getBaseAPIURL();

export const videoServices = {
  fetchVideos: () => {
    return axiosInstance.get(`${baseAPIURL}/api/v1//shorts/videos/`);
  },
  FetchVideoPrivicy: () => {
    return axiosInstance.get(
      `${baseAPIURL}/api/v1//shorts/videos/choice-fields/`
    );
  },
  createVideos: (data: VideoCredentials) => {
    return axiosInstance.post(`${baseAPIURL}/api/v1//shorts/videos/`, data);
  },
};
