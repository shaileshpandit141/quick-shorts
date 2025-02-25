import { getEnv } from "./getEnv";

export const buildMediaURL = (relativeMediaUrl: string): string => {
  const BASE_MEDIA_URL = getEnv("BASE_MEDIA_URL").replace(/\/+$/, "");
  return `${BASE_MEDIA_URL}/${relativeMediaUrl.replace(/^\/+/, "")}`;
};
