import React from 'react'
import './Signup.css'
import { Link } from 'react-router-dom'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'
import Input from 'components/common/input/Input'
import useFormDataChange from 'hooks/useFormDataChange'
import SignupWrapper from './SignupWrapper'

const Signup: React.FC = (props) => {
  
  const [formData, handleFormDataChange] = useFormDataChange({
    email: '',
    password: '',
    confirm_password: ''
  })

  const handleFormSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    console.log(formData)
  }

  return (
    <SignupWrapper>
      <form onSubmit={handleFormSubmit}>
        <Input
          name='email'
          type='text'
          value={formData.email}
          onChange={handleFormDataChange}
        />
        <Input
          name='password'
          type='password'
          value={formData.password}
          onChange={handleFormDataChange}
        />
        <Input
          name='confirm_password'
          type='password'
          value={formData.confirm_password}
          onChange={handleFormDataChange}
        />
        <div className='right-section-row'>
          <Link to='/signin' className='link'>
            <span className='icon'>
              <LazyIconImport icon='signin' />
            </span>
            <span className='label'>Sign in</span>
          </Link>
          <button className='button'>
            <span className='icon'>
              <LazyIconImport icon='signup' />
            </span>
            <span className='label'>Sign up</span>
          </button>
        </div>
      </form>
    </SignupWrapper>
  )
}

export default Signup
