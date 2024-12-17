import React from 'react'
import './SigninForm.css'
import { Navigate } from 'react-router-dom'
import { Input } from 'components'
import ForgotPasswordLink from './Actions/ForgotPasswordLink/ForgotPasswordLink'
import SignupLink from './Actions/SignupLink/SignupLink'
import authActions from 'features/auth'
import { useDispatch } from 'react-redux'
import { DisplayErrors } from 'components'
import useFormDataChange from 'hooks/useFormDataChange'
import { SigninCredentials } from 'API/API.types'
import { ActionButton } from 'components'

const SigninForm: React.FC = (props) => {

  const dispatch = useDispatch()
  const { status, message, errors } = authActions.useSigninSelector()
  const [formData, handleFormDataChange] = useFormDataChange<SigninCredentials>({
    email: '',
    password: ''
  })

  if (status === 'succeeded') {
    return <Navigate to='/home' />
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    dispatch(
      authActions.signinThunk(formData) as any
    )
  }

  return (
    <form
      className='signin-form'
      onSubmit={handleSubmit}
    >
      <Input
        name='email'
        type='text'
        value={formData.email}
        onChange={handleFormDataChange}
        isDisabled={status === 'loading'}
        errorMessage={
          (errors.email === undefined) ? undefined : errors.email
        }
      />
      <Input
        name='password'
        type='password'
        value={formData.password}
        onChange={handleFormDataChange}
        isDisabled={status === 'loading'}
        errorMessage={
          (errors.password === undefined) ? undefined : errors.password
        }
      />
      {(errors.non_field_errors !== undefined)
        && <DisplayErrors message={errors.non_field_errors} />
      }
      <div className='actions'>
        <span></span>
        <ForgotPasswordLink />
      </div>
      <div className='actions'>
        <SignupLink />
        <ActionButton
          icon='signin'
          isLoaderOn={status === 'loading'}
        >
          Sign in
        </ActionButton>
      </div>
    </form>
  )
}

export default SigninForm
