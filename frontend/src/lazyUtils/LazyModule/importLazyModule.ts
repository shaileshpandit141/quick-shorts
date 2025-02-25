import React from "react";

/**
 * Helper function that wraps dynamic imports with retry logic
 * @param importFunction - Dynamic import function to be called
 * @param retries - Number of retries on failure (default: 3)
 * @param delay - Delay between retries in ms (default: 1000)
 */
export const importLazyModule = (
  importFunction: () => Promise<any>,
  retries: number = 3,
  delay: number = 1000,
) =>
  React.lazy(
    () =>
      new Promise((resolve, reject) => {
        const tryImport = async (attempt = 0): Promise<void> => {
          try {
            const result = await importFunction();
            resolve(result);
          } catch (error) {
            if (attempt < retries) {
              console.warn(
                `Retrying import: attempt ${attempt + 1} of ${retries}`,
              );
              await new Promise((r) => setTimeout(r, delay));
              return tryImport(attempt + 1);
            }
            reject(error);
          }
        };

        tryImport();
      }),
  );
