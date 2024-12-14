import React from 'react'
import { ErrorBoundary as ReactErrorBoundary, FallbackProps } from 'react-error-boundary'
import './ErrorBoundary.css'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'

const ErrorFallback = ({ error, resetErrorBoundary }: FallbackProps) => (
  <div className='inner-grid-2-2 error-boundary' role="alert">
    <div className="inner-error-boundary">
      <h4>Something went wrong</h4>
      <p>
        {
          error?.message && (
            <>
              <span>Message:</span>
              {error.message}
            </>
          )
        }
      </p>
      <button
        className='button'
        onClick={resetErrorBoundary}
      >
        <span className='icon'>
          <LazyIconImport icon='reTry' />
        </span>
        <span className='label'>
          Try again
        </span>
      </button>
    </div>
  </div>
)

const ErrorBoundary = ({ children }: { children: React.ReactNode }) => (
  <ReactErrorBoundary FallbackComponent={ErrorFallback}>
    {children}
  </ReactErrorBoundary>
)

export default ErrorBoundary
