import React from 'react'
import './SignupForm.css'
import Input from 'components/common/input/Input'
import useSignupFormFields from '../hooks/useSignupFormFileds'
import SignupActions from './SignupActions/SignupActions'

const SignupForm: React.FC = (props) => {

  const [formFields, formData] = useSignupFormFields()

  const handleFormSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    console.log(formData)
  }

  const fields = formFields.map((field, index) => (
    <Input
      key={index}
      {...field}
    />
  ))

  return (
    <form
      className='signup-form'
      onSubmit={handleFormSubmit}
    >
      {fields}
      <SignupActions />
    </form>
  )
}

export default SignupForm
