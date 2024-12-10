import React, { Suspense } from 'react';
import ErrorBoundary from 'components/common/errorBoundary/ErrorBoundary';

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

export const LazyModuleLoader: React.FC<{
  element: React.ReactNode;
  fallback: React.ReactNode;
}> = ({ element, fallback }) => (
  <ErrorBoundary>
    <Suspense fallback={fallback}>
      {element}
    </Suspense>
  </ErrorBoundary>
);
