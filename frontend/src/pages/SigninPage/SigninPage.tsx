import React, { useEffect } from 'react';
import './SigninPage.css';
import { Link, Navigate, useNavigate } from 'react-router-dom';
import { useFormDataChange } from 'hooks';
import { isAuthenticated } from 'utils';
import { Input, DisplayFormErrors, Button, SignupLink } from 'components';
import { signinUser, resetSigninUser, useSigninUserSelector } from 'features/auth/signin';
import { SigninCredentials } from 'services/authServices';
import { triggerToast } from 'features/toast';

const SigninPage: React.FC = () => {

  const navigate = useNavigate()
  const { status, message, errors } = useSigninUserSelector()
  const [formData, handleFormDataChange] = useFormDataChange<SigninCredentials>({
    email: '',
    password: ''
  })

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    signinUser(formData)
  }

  useEffect(() => {
    if (status === "succeeded") {
      triggerToast("success", message)
      navigate("/home")
    } else if (status === "failed") {
      triggerToast("error", message)
      resetSigninUser();
    }
  }, [status, message, navigate])

  if (isAuthenticated()) {
    return <Navigate to="/home" />
  }

  return (
    <div className='signin-page'>
      <div className='header'>
        <h3 className='form-label'>Sign in</h3>
        <p className='form-description'>
          Sign in with your existing credentials.
        </p>
      </div>
      <form
        className='form'
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
        <DisplayFormErrors field={'none'} errors={errors} />
        <div className='split-container'>
          <span></span>
          <Link
            to='/forgot-password'
          >Forgot password</Link>
        </div>
        <div className='actions'>
          <SignupLink />
          <Button
            type='submit'
            iconName='signin'
            className='button'
            isLoaderOn={status === 'loading'}
          >sign in</Button>
        </div>
      </form>
    </div>
  )
}

export default SigninPage
