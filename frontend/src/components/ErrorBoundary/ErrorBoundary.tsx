import React from 'react'
import {
  ErrorBoundary as ReactErrorBoundary,
  FallbackProps
} from 'react-error-boundary'
import './ErrorBoundary.css'
import Button from 'components/Button/Button'
import { LazyIcon } from 'lazyUtils/LazyIcon/LazyIcon'

const ErrorFallback = ({ error, resetErrorBoundary }: FallbackProps) => (
  <div className='inner-grid-2-2 error-boundary' role="alert">
    <div className='error-boundary-component'>
      <Button
        type='button'
        iconName='info'
        title={error?.message}
      >Something went wrong</Button>
      <Button
        type='icon'
        iconName='reTry'
        onClick={resetErrorBoundary}
        title='re try'
      />
    </div>
  </div>
)

const ErrorBoundary = ({ children }: { children: React.ReactNode }) => (
  <ReactErrorBoundary FallbackComponent={ErrorFallback}>
    {children}
  </ReactErrorBoundary>
)

export default ErrorBoundary
