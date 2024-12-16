import React from 'react'
import './SigninForm.css'
import { Navigate } from 'react-router-dom'
import { Input } from 'components'
import { isAuthenticated } from 'utils/isAuthenticted'
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
  const { status, message, errors } = authActions.useSigninSelector()

  if (status === 'succeeded' || isAuthenticated()) {
    return <Navigate to='/home' />
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    dispatch(
      authActions.signinThunk(formData) as any
    )
  }

  const fields = formFields.map((field, index) => (
    <div key={index} className='fields-container'>
      <Input
        key={index}
        {...field}
        isDisabled={status === 'loading'}
        errorMessage={
          (status === 'failed' && errors?.email) && errors.email
            (status === 'failed' && errors?.password) && errors.password
        }
      />
    </div>
  ))

  return (
    <form
      className='signin-form'
      onSubmit={handleSubmit}
    >
      {fields}
      {(status === 'failed' && errors?.non_field_errors)
        && <DisplayErrors message={errors.non_field_errors} />
      }
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
