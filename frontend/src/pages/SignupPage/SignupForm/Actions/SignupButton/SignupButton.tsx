import React from 'react'
import './SignupButton.css'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'

const SignupButton: React.FC = (props) => {
  return (
    <button className='button signup-action-button'>
      <span className='icon'>
        <LazyIconImport icon='signup' />
      </span>
      <span className='label'>Sign up</span>
    </button>
  )
}

export default SignupButton
