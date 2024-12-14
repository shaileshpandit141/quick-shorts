import React from 'react'
import './ForgotPasswordLink.css'
import { Link } from 'react-router-dom'

const ForgotPasswordLink: React.FC = (props) => {
  return (
    <Link
      to='/forgot-password'
      className='forgot-password-link'
    >
      forgot password
    </Link>
  )
}

export default ForgotPasswordLink
