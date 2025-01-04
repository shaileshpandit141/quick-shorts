import React, { useEffect } from 'react'
import './SigninPage.css'
import { Navigate } from 'react-router-dom'
import { useDispatch } from 'react-redux'
import { resetSigninState } from 'features/auth'
import { isAuthenticated } from 'utils/isAuthenticted'
import SigninHeader from './SigninHeader/SigninHeader'
import SigninForm from './SigninForm/SigninForm'

const SigninPage: React.FC = (props) => {
  const dispatch = useDispatch()

  useEffect(() => {
    dispatch(resetSigninState())
  });

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
