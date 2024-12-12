import React from 'react'
import './SignupActions.css'
import { Link } from 'react-router-dom'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'

const SignupActions: React.FC = (props) => {
  return (
    <div className='signup-actions'>
      <Link to='/signin' className='link'>
        <span className='icon'>
          <LazyIconImport icon='signin' />
        </span>
        <span className='label'>Sign in</span>
      </Link>
      <button className='button'>
        <span className='icon'>
          <LazyIconImport icon='signup' />
        </span>
        <span className='label'>Sign up</span>
      </button>
    </div>
  )
}

export default SignupActions
