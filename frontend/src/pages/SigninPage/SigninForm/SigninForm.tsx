import React from 'react'
import './SigninForm.css'
import { Navigate, Link } from 'react-router-dom'
import { Input } from 'components'
import { AnchorLink } from 'components'
import authActions from 'features/auth'
import { useDispatch } from 'react-redux'
import { DisplayErrors } from 'components'
import useFormDataChange from 'hooks/useFormDataChange'
import { SigninCredentials } from 'API/API.types'
import { ActionButton } from 'components'

const SigninForm: React.FC = (props) => {

  const dispatch = useDispatch()
  const { status, errors } = authActions.useSigninSelector()
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
        <Link
          to='/forgot-password'
          className='forgot-password-link'
        >
          forgot password
        </Link>
      </div>
      <div className='actions'>
        <AnchorLink
          to="/sign-up"
          type="link"
          icon='signin'
          className='sign-link'
        >
          sign up
        </AnchorLink>
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
