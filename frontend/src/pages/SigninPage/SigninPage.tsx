import React from 'react'
import './SigninPage.css'
import { Navigate } from 'react-router-dom'
import { isAuthenticated } from 'features/auth'
import SigninHeader from './SigninHeader/SigninHeader'
import SigninForm from './SigninForm/SigninForm'

const SigninPage: React.FC = (props) => {
  if (isAuthenticated()) {
    return (
      <Navigate to={'/home'} />
    )
  }

  return (
    <div className='signin-page'>
      <SigninHeader />
      <SigninForm />
    </div>
  )
}

export default SigninPage
