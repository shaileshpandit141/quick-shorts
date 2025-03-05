import { JWTTokenHandler } from "utils/JWTTokenHandler";

const getRefreshToken = (): string | null => {
  try {
    return localStorage.getItem("refresh_token");
  } catch (error) {
    console.error("Error accessing localStorage:", error);
    return null;
  }
};

export const isUserAuthenticated = (): boolean => {
  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    return false;
  }

  const handler = new JWTTokenHandler(refreshToken);
  return !handler.isTokenExpired();
};
