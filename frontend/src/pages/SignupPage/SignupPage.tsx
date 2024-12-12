import React from 'react'
import './SignupPage.css'
import SignupHeader from './SignupHeader/SignupHeader'
import SignupForm from './SignupForm/SignupForm'

const SignupPage: React.FC = (props) => {
  return (
    <div className='signup-page'>
      <SignupHeader />
      <SignupForm />
    </div>
  )
}

export default SignupPage
