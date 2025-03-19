import { getEnv } from "utils/getEnv";

export const getBaseAPIURL = (): string => {
  return getEnv("BASE_API_URL");
};
