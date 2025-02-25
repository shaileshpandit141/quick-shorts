export const getEnv = (key: string, fallback?: string): string => {
  const value = process.env[`REACT_APP_${key}`];

  if (!value) {
    if (fallback !== undefined) return fallback;
    throw new Error(`Missing environment variable: REACT_APP_${key}`);
  }

  return value;
};
