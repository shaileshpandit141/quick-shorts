import React, { Suspense } from "react";
import { ErrorBoundary } from "components";

/**
 * Props interface for RenderLazyModule component
 */
interface RenderLazyModuleProps {
  element: React.ReactNode;
  fallback: React.ReactNode;
}

/**
 * Component that handles lazy loading with error boundaries and loading states
 */
export const RenderLazyModule = ({
  element,
  fallback,
}: RenderLazyModuleProps): JSX.Element => {
  return (
    <ErrorBoundary>
      <Suspense fallback={fallback}>{element}</Suspense>
    </ErrorBoundary>
  );
};
