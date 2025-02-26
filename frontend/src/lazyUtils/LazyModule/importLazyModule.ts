import React from "react";

/**
 * Helper function that dynamically imports a module with retry logic.
 * It supports both default and named exports, and auto-detects the export name when possible.
 *
 * @param importFunction - Dynamic import function
 * @param retries - Number of retries on failure (default: 3)
 * @param delay - Delay between retries in ms (default: 1000)
 */
export const importLazyModule = <T extends Record<string, any>>(
  importFunction: () => Promise<T>,
  retries: number = 3,
  delay: number = 1000,
) =>
  React.lazy(
    () =>
      new Promise<{ default: T[keyof T] }>((resolve, reject) => {
        const tryImport = async (attempt = 0): Promise<void> => {
          try {
            const module = await importFunction();

            // Extract only the file name, removing directories and extensions
            const match = importFunction.toString().match(/import\("(.+?)"\)/);
            const filePath = match ? match[1] : null;
            const fileName =
              filePath
                ?.split("/")
                .pop()
                ?.replace(/\.[^/.]+$/, "") || null;

            if (module.default) {
              resolve({ default: module.default }); // Default export found
            } else if (fileName && module[fileName]) {
              resolve({ default: module[fileName] }); // Named export found
            } else {
              // Detect first available named export (useful for re-exports from index.ts)
              const firstKey = Object.keys(module)[0];
              if (firstKey) {
                console.warn(
                  `importLazyModule Warning: No exact match for '${fileName}', using '${firstKey}' instead.`,
                );
                resolve({ default: module[firstKey] }); // Use first named export as fallback
              } else {
                reject(
                  new Error(
                    `importLazyModule Error: No matching export found in '${filePath}'. 
                   Ensure the module has a default export or at least one named export.`,
                  ),
                );
              }
            }
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
