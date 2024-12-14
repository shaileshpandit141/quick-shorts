import React from 'react'
import './SigninForm.css'
import Input from 'components/common/input/Input'
import useSigninFormFields from './hooks/useSigninFormFileds'
import ForgotPasswordLink from './Actions/ForgotPasswordLink/ForgotPasswordLink'
import SignupLink from './Actions/SignupLink/SignupLink'
import SigninButton from './Actions/SigninButton/SigninButton'

const SigninForm: React.FC = (props) => {

  const [formFields, formData] = useSigninFormFields()

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    console.log(formData)
  }

  const fields = formFields.map((field, index) => (
    <Input
      key={index}
      {...field}
    />
  ))

  return (
    <form
      className='signin-form'
      onSubmit={handleSubmit}
    >
      {fields}
      <div className='actions'>
        <span></span>
        <ForgotPasswordLink />
      </div>
      <div className='actions'>
        <SignupLink />
        <SigninButton />
      </div>
    </form>
  )
}

export default SigninForm
