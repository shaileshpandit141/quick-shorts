import React, { useEffect } from 'react'
import './SignupForm.css'
import { Input } from 'components'
import { AnchorLink, Button } from 'components'
import {
  signupThunk,
  useSignupSelector,
  resetSignupState
} from 'features/auth'
import { useDispatch } from 'react-redux'
import { DisplayFormErrors } from 'components'
import { useFormDataChange } from 'hooks/useFormDataChange'
import { SignupCredentials } from 'API/API.types'
import { triggerToast } from 'features/toast'

const SignupForm: React.FC = (props) => {

  const dispatch = useDispatch()
  const { status, message, errors, data } = useSignupSelector()
  const [formData, handleFormDataChange] = useFormDataChange<SignupCredentials>({
    email: '',
    password: '',
    confirm_password: '',
  })

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    dispatch(
      signupThunk(formData) as any
    )
  }

  useEffect(() => {
    dispatch(resetSignupState())
    if (status === "succeeded") {
      triggerToast(dispatch, "success", message)
    } else if (status === "failed") {
      triggerToast(dispatch, "error", message)
    }
  }, [dispatch, message, status])


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
        <AnchorLink
          to="/sign-in"
          type="link"
          iconName='signin'
          className='signin-link'
        >
          sign in
        </AnchorLink>
        <Button
          type='submit'
          iconName='signup'
          label='Sign up'
          className='signup-button'
          isLoaderOn={status === 'loading'}
          isDisabled={status === 'succeeded'}
        />
      </div>
    </form>
  )
}

export default SignupForm
