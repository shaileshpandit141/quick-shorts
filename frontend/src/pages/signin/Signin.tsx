import React from 'react'
import './Signin.css'
import { Link } from 'react-router-dom'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'
import Input from 'components/common/input/Input'
import useFormDataChange from 'hooks/useFormDataChange'
import SigninWrapper from './SigninWrapper'

const Signin: React.FC = (props) => {

  const [formData, handleFormDataChange] = useFormDataChange({
    email: '',
    password: ''
  })

  const handleFormSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    console.log(formData)
  }

  return (
    <SigninWrapper>
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
        <div className='right-section-row for-right-links'>
          <Link to='/forgot-password' >forgot password</Link>
        </div>
        <div className='right-section-row'>
          <Link to='/signup' className='link'>
            <span className='icon'>
              <LazyIconImport icon='signup' />
            </span>
            <span className='label'>Sign up</span>
          </Link>
          <button className='button'>
            <span className='icon'>
              <LazyIconImport icon='signin' />
            </span>
            <span className='label'>Sign in</span>
          </button>
        </div>
      </form>
    </SigninWrapper>
  )
}

export default Signin
