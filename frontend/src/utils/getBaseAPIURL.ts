import { getEnv } from "./getEnv";

export const getBaseAPIURL = (): string => {
  return getEnv("BASE_MEDIA_URL");
};
