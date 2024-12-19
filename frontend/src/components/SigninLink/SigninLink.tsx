import React from 'react'
import './SigninLink.css'
import { Link } from 'react-router-dom'
import { isAuthenticated } from 'utils/isAuthenticted'

const SigninLink: React.FC = (props) => {
  if (isAuthenticated()) {
    return null
  }
  return (
    <Link to={'/signin'} className='link'>Sign in</Link>
  )
}

export default SigninLink
