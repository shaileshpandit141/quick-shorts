import React from 'react'
import './SigninButton.css'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'
import { Loader } from 'components'

interface SigninButtonProps {
  status: "failed" | "succeeded" | "idle" | "loading"
}

const SigninButton: React.FC<SigninButtonProps> = (props) => {
  const { status } = props

  if (status === 'loading') {
    return (
      <button
        className='button signin-action-button'
        disabled
      >
        <span className='icon'>
          <Loader />
        </span>
        <span className='label'>Sign in</span>
      </button>
    )
  }

  return (
    <button className='button signin-action-button'>
      <span className='icon'>
        <LazyIconImport icon='signin' />
      </span>
      <span className='label'>Sign in</span>
    </button>
  )
}

export default SigninButton
