import React from 'react'
import {
  ErrorBoundary as ReactErrorBoundary,
  FallbackProps
} from 'react-error-boundary'
import './ErrorBoundary.css'
import { LazyIcon } from 'lazyUtils/LazyIcon/LazyIcon'

const ErrorFallback = ({ error, resetErrorBoundary }: FallbackProps) => (
  <div className='inner-grid-2-2 error-boundary' role="alert">
    <div className='error-boundary-component'>
      <button
        className='button'
        title={error?.message}
      >
        <span className='icon'>
          <LazyIcon iconName='info' />
        </span>
        <span className='label'>
          Something went wrong
        </span>
      </button>
      <button
        className='button'
        onClick={resetErrorBoundary}
      >
        <span className='icon'>
          <LazyIcon iconName='reTry' />
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
