import React, { useEffect } from 'react';
import './SigninPage.css';
import { isAuthenticated } from 'utils';
import { Navigate, Link } from 'react-router-dom';
import { Input, DisplayFormErrors, Button, SignupLink } from 'components';
import {
  dispatchSigninAction,
  useSigninSelector
} from 'features/auth/signin';
import { dispatchRestSignoutState } from 'features/auth/signout';
import { useFormDataChange } from 'hooks/useFormDataChange';
import { SigninCredentials } from 'services/authServices';
import { triggerToast } from 'features/toast';

const SigninPage: React.FC = (props) => {
  const { status, message, errors } = useSigninSelector()
  const [formData, handleFormDataChange] = useFormDataChange<SigninCredentials>({
    email: '',
    password: ''
  })

  useEffect(() => {
    dispatchRestSignoutState();
    if (status === "succeeded") {
      triggerToast("success", message)
    } else if (status === "failed") {
      triggerToast("error", message)
    }
  }, [message, status])

  if (status === 'succeeded' || isAuthenticated()) {
    return <Navigate to='/home' />
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    dispatchSigninAction(formData)
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
