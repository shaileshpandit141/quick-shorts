import React, { useEffect } from 'react'
import './SignupForm.css'
import { Input } from 'components'
import { AnchorLink } from 'components'
import {
  signupThunk,
  useSignupSelector,
  resetSignupState
} from 'features/auth'
import { useDispatch } from 'react-redux'
import { DisplayErrors } from 'components'
import { useFormDataChange } from 'hooks/useFormDataChange'
import { SignupCredentials } from 'API/API.types'
import { SubmitButton } from 'components'

const SignupForm: React.FC = (props) => {

  const dispatch = useDispatch()
  const { status, errors, data } = useSignupSelector()
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
    dispatch(
      resetSignupState()
    )
  }, [dispatch]);

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
        errorMessage={errors?.email
          && errors.email
        }
      />
      <Input
        name='password'
        type='password'
        value={formData.password}
        onChange={handleFormDataChange}
        isDisabled={status === 'loading' || status === 'succeeded'}
        errorMessage={errors?.password
          && errors.password
        }
      />
      <Input
        name='confirm_password'
        type='password'
        value={formData.confirm_password}
        onChange={handleFormDataChange}
        isDisabled={status === 'loading' || status === 'succeeded'}
        errorMessage={errors?.confirm_password
          && errors.confirm_password
        }
      />
      {errors?.non_field_errors
        && <DisplayErrors message={errors.non_field_errors} />
      }
      {data?.detail && (
        <p>{data.detail}</p>
      )}
      <div className='actions'>
        <AnchorLink
          to="/sign-in"
          type="link"
          icon='signin'
          className='signin-link'
        >
          sign in
        </AnchorLink>
        <SubmitButton
          icon='signup'
          isLoaderOn={status === 'loading'}
          isDisabled={status === 'succeeded'}
        >
          Sign up
        </SubmitButton>
      </div>
    </form>
  )
}

export default SignupForm
