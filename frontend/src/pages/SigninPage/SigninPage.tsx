import React from 'react'
import './SigninPage.css'
import SigninHeader from './SigninHeader/SigninHeader'
import SigninForm from './SigninForm/SigninForm'

const SigninPage: React.FC = (props) => {
  return (
    <div className='signin-page'>
      <SigninHeader />
      <SigninForm />
    </div>
  )
}

export default SigninPage
