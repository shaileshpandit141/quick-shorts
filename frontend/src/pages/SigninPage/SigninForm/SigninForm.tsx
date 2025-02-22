import React, { useEffect } from 'react'
import './SigninForm.css'
import { Navigate, Link } from 'react-router-dom'
import { Input } from 'components'
import { NavLink } from 'components'
import {
  dispatchSigninAction,
  useSigninSelector
} from 'features/auth/signin'
import { dispatchRestSignoutState } from 'features/auth/signout'
import { DisplayFormErrors } from 'components'
import { useFormDataChange } from 'hooks/useFormDataChange'
import { SigninCredentials } from 'services/authServices'
import { Button } from 'components'
import { triggerToast } from 'features/toast'

const SigninForm: React.FC = () => {

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

  if (status === 'succeeded') {
    return <Navigate to='/home' />
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    dispatchSigninAction(formData)
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
      <DisplayFormErrors field={'none'} errors={errors} />
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
        <NavLink
          to="/sign-up"
          type="link"
          iconName='signin'
          className='sign-link'
        >sign up</NavLink>
        <Button
          type='submit'
          iconName='signin'
          className='signin-button'
          isLoaderOn={status === 'loading'}
        >sign in</Button>
      </div>
    </form>
  )
}

export default SigninForm
