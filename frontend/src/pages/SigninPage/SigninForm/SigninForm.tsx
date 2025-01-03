import React from 'react'
import './SigninForm.css'
import { Navigate, Link } from 'react-router-dom'
import { Input } from 'components'
import { AnchorLink } from 'components'
import { signinThunk, useSigninSelector } from 'features/auth'
import { useDispatch } from 'react-redux'
import { DisplayErrors } from 'components'
import { useFormDataChange } from 'hooks/useFormDataChange'
import { SigninCredentials } from 'API/API.types'
import { Button } from 'components'

const SigninForm: React.FC = (props) => {

  const dispatch = useDispatch()
  const { status, errors } = useSigninSelector()
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
      signinThunk(formData) as any
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
      />
      <Input
        name='password'
        type='password'
        value={formData.password}
        onChange={handleFormDataChange}
        isDisabled={status === 'loading'}
      />
      {errors?.non_field_errors
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
          iconName='signin'
          className='sign-link'
        >
          sign up
        </AnchorLink>
        <Button
          type='submit'
          iconName='signin'
          label='Sign in'
          className='signin-button'
          isLoaderOn={status === 'loading'}
        />
      </div>
    </form>
  )
}

export default SigninForm
