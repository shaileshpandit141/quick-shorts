import { axiosInstance } from "axiosInstance";
import { getBaseAPIURL } from "utils/getBaseAPIURL";
import { CommentParams, CommentCredentials } from "./commentServices.types";

const baseAPIURL = getBaseAPIURL();

export const commentsServices = {
  fetchComments: (params: CommentParams) => {
    const queryString = new URLSearchParams(
      Object.entries(params).reduce(
        (acc, [key, value]) => {
          acc[key] = String(value);
          return acc;
        },
        {} as Record<string, string>
      )
    ).toString();
    return axiosInstance.get(
      `${baseAPIURL}/api/v1//shorts/comments/?${queryString}`
    );
  },
  createVideos: (comment: CommentCredentials) => {
    return axiosInstance.post(`${baseAPIURL}/api/v1//shorts/videos/`, comment);
  },
};
