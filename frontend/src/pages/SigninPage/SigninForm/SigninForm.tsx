import React from 'react'
import './SigninForm.css'
import { Input } from 'components'
import useSigninFormFields from './hooks/useSigninFormFileds'
import ForgotPasswordLink from './Actions/ForgotPasswordLink/ForgotPasswordLink'
import SignupLink from './Actions/SignupLink/SignupLink'
import SigninButton from './Actions/SigninButton/SigninButton'
import authActions from 'features/auth'
import { useDispatch } from 'react-redux'
import { DisplayErrors } from 'components'

const SigninForm: React.FC = (props) => {

  const [formFields, formData] = useSigninFormFields()
  const dispatch = useDispatch()
  const { status, message, errors, data } = authActions.useSigninSelector()

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    dispatch(
      authActions.signinThunk(formData) as any
    )
  }

  const fields = formFields.map((field, index) => (
    <>
      <Input
        key={index}
        {...field}
        isDisabled={status === 'loading'}
      />
    </>
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
        <SigninButton status={status} />
      </div>
    </form>
  )
}

export default SigninForm
