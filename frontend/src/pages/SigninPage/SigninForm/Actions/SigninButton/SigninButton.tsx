import React from 'react'
import './SigninButton.css'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'

const SigninButton: React.FC = (props) => {
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
