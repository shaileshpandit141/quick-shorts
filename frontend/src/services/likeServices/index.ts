import { axiosInstance } from "axiosInstance";
import { getBaseAPIURL } from "utils/getBaseAPIURL";
import { LikeCredentials } from "./likeServices.types";

const baseAPIURL = getBaseAPIURL();

export const commentsServices = {
  likeCreate: (credentials: LikeCredentials) => {
    return axiosInstance.post(
      `${baseAPIURL}/api/v1//shorts/likes/`,
      credentials
    );
  },
  likeDelete: (video_id: number) => {
    return axiosInstance.delete(
      `${baseAPIURL}/api/v1//shorts/likes/${video_id}/`
    );
  },
};
