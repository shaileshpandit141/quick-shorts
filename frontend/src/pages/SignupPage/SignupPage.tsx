import React, { useEffect } from 'react'
import './SignupPage.css'
import { Input, NavLink, Button, DisplayFormErrors, SigninLink } from 'components'
import {
  dispatchSignupAction,
  dispatchRestSigupState,
  useSignupSelector
} from 'features/auth/signup';
import { useFormDataChange } from 'hooks/useFormDataChange'
import { SignupCredentials } from 'services/authServices'
import { triggerToast } from 'features/toast'

const SignupPage: React.FC = (props) => {

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
    if (status === "succeeded") {
      triggerToast("success", message)
      dispatchRestSigupState()
    } else if (status === "failed") {
      triggerToast("error", message)
    }
  }, [message, status])

  return (
    <div className='signup-page'>
      <div className='header'>
        <h3 className='form-label'>Sign up</h3>
        <p className='form-description'>
          Join us by creating your account.
        </p>
      </div>
      <form
        className='form'
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
          <SigninLink />
          <Button
            type='submit'
            iconName='signup'
            className='button'
            isLoaderOn={status === 'loading'}
            isDisabled={status === 'succeeded'}
          >sign up</Button>
        </div>
      </form>
    </div>
  )
}

export default SignupPage
