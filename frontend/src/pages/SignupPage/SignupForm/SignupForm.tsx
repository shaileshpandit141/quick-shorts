import React, { useEffect } from 'react';
import './SignupForm.css';
import { Input, NavLink, Button, DisplayFormErrors } from 'components';
import {
  dispatchSignupAction,
  dispatchRestSigupState,
  useSignupSelector
} from 'features/auth/signup';
import { useFormDataChange } from 'hooks/useFormDataChange'
import { SignupCredentials } from 'services/authServices'
import { triggerToast } from 'features/toast'

const SignupForm: React.FC = (props) => {
  
  const { status, message, errors, data } = useSignupSelector()
  const [formData, handleFormDataChange] = useFormDataChange<SignupCredentials>({
    email: '',
    password: '',
    confirm_password: '',
  })

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    dispatchSignupAction(formData)
  }

  useEffect(() => {
    dispatchRestSigupState()
    if (status === "succeeded") {
      triggerToast("success", message)
    } else if (status === "failed") {
      triggerToast("error", message)
    }
  }, [message, status])


  return (
    <form
      className='signup-form'
      onSubmit={handleSubmit}
    >
      <Input
        name='email'
        type='email'
        value={formData.email}
        onChange={handleFormDataChange}
        isDisabled={status === 'loading' || status === 'succeeded'}
        errors={errors}
      />
      <Input
        name='password'
        type='password'
        value={formData.password}
        onChange={handleFormDataChange}
        isDisabled={status === 'loading' || status === 'succeeded'}
        errors={errors}
      />
      <Input
        name='confirm_password'
        type='password'
        value={formData.confirm_password}
        onChange={handleFormDataChange}
        isDisabled={status === 'loading' || status === 'succeeded'}
        errors={errors}
      />
      <DisplayFormErrors field={'none'} errors={errors} />
      {data?.detail && (
        <p>{data.detail}</p>
      )}
      <div className='actions'>
        <NavLink
          to="/sign-in"
          type="link"
          iconName='signin'
          className='signin-link'
        >sign in</NavLink>
        <Button
          type='submit'
          iconName='signup'
          className='signup-button'
          isLoaderOn={status === 'loading'}
          isDisabled={status === 'succeeded'}
        >sign up</Button>
      </div>
    </form>
  )
}

export default SignupForm
