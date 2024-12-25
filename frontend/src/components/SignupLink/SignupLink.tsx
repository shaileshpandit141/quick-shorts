import React from 'react'
import './SignupLink.css'
import { Link } from 'react-router-dom'
import { isAuthenticated } from 'utils/isAuthenticted'

const SignupLink: React.FC = (props) => {
  if (isAuthenticated()) {
    return null
  }
  return (
    <Link to={'/sign-up'} className='link'>Sign up</Link>
  )
}

export default SignupLink
