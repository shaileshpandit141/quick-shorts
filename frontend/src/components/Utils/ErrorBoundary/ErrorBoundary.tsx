import React, { FC, JSX } from "react";
import {
  ErrorBoundary as ReactErrorBoundary,
  FallbackProps,
} from "react-error-boundary";
import "./ErrorBoundary.css";
import Button from "components/Common/Button/Button";

const ErrorFallback = ({ error, resetErrorBoundary }: FallbackProps) => (
  <div className="inner-grid-2-2 error-boundary" role="alert">
    <div className="error-boundary-component">
      <Button type="button" icon="info" title={error?.message}>
        Something went wrong!
      </Button>
      <Button
        type="button"
        icon="reTry"
        onClick={resetErrorBoundary}
        title="re try"
      >
        re-try
      </Button>
    </div>
  </div>
);

interface ErrorBoundaryProps {
  children: React.ReactNode;
}

const ErrorBoundary: FC<ErrorBoundaryProps> = ({ children }): JSX.Element => {
  return (
    <ReactErrorBoundary FallbackComponent={ErrorFallback}>
      {children}
    </ReactErrorBoundary>
  )
};

export default ErrorBoundary;
