import React, { Suspense } from 'react';
import { ErrorBoundary } from 'components';

/**
 * Props interface for LazyModuleLoader component
 */
interface LazyModuleLoaderProps {
  element: React.ReactNode;
  fallback: React.ReactNode;
}

/**
 * Helper function that wraps dynamic imports with retry logic
 * @param importFunction - Dynamic import function to be called
 * @param retries - Number of retries on failure (default: 3)
 * @param delay - Delay between retries in ms (default: 1000)
 */
export const lazyModuleImport = (
  importFunction: () => Promise<any>,
  retries: number = 3,
  delay: number = 1000
) => React.lazy(() =>
  new Promise((resolve, reject) => {
    const tryImport = async (attempt = 0): Promise<void> => {
      try {
        const result = await importFunction();
        resolve(result);
      } catch (error) {
        if (attempt < retries) {
          console.warn(`Retrying import: attempt ${attempt + 1} of ${retries}`);
          await new Promise(r => setTimeout(r, delay));
          return tryImport(attempt + 1);
        }
        reject(error);
      }
    };

    tryImport();
  })
);

/**
 * Component that handles lazy loading with error boundaries and loading states
 */
export const LazyModuleLoader = (
  { element, fallback }: LazyModuleLoaderProps
): JSX.Element => {
  return (
    <ErrorBoundary>
      <Suspense fallback={fallback}>
        {element}
      </Suspense>
    </ErrorBoundary>
  );
};
