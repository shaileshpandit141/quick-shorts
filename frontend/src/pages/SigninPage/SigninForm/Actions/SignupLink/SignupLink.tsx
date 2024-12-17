import React from 'react'
import './SignupLink.css'
import { Link } from 'react-router-dom'
import { LazyIconImport } from 'lazyUtils/LazyIconImport/LazyIconImport'

const SignupLink: React.FC = (props) => {
  return (
    <Link to='/signup' className='link signup-action-link'>
      <span className='icon'>
        <LazyIconImport icon='signup' />
      </span>
      <span className='label'>Sign up</span>
    </Link>
  )
}

export default SignupLink
