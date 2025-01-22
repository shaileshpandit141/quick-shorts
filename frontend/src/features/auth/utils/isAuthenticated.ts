const getRefreshToken = (): string | null => {
  try {
    return localStorage.getItem('refresh_token');
  } catch (error) {
    console.error('Error accessing localStorage:', error);
    return null;
  }
};

export const isAuthenticated = (): boolean => {
  const refresh_token = getRefreshToken();
  return Boolean(refresh_token);
};
