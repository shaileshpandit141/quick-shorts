import React from 'react'
import './SigninLink.css'
import { Link } from 'react-router-dom'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'

const SigninLink: React.FC = (props) => {
  return (
    <Link to='/signin' className='link signin-action-link'>
      <span className='icon'>
        <LazyIconImport icon='signin' />
      </span>
      <span className='label'>Sign in</span>
    </Link>
  )
}

export default SigninLink
