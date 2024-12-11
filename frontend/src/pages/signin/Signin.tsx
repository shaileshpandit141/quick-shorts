import React from 'react'
import './Signin.css'
import { Link } from 'react-router-dom'
import AppLogo from 'components/common/appLogo/AppLogo'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'
import Input from 'components/common/input/Input'
import useFormDataChange from 'hooks/useFormDataChange'

const Signin: React.FC = () => {

  const [formData, handleFormDataChange] = useFormDataChange({
    email: '',
    password: ''
  })

  const handleFormSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    console.log(formData)
  }

  return (
    <div className='signin-page'>
      <section className='left-section'>
        <AppLogo size={60} />
        <h3 className='signin-label'>Sign in</h3>
        <p className='discription'>
          use your existing account
        </p>
        <Link to='../' className='link back-link'>
          <span className='icon'>
            <LazyIconImport icon='arrowBack' />
          </span>
          <span className='label'>Back</span>
        </Link>
      </section>
      <form
        className='right-section'
        onSubmit={handleFormSubmit}
      >
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
        <div className='right-section-row'>
          <Link to='/forgot-password' className='forgot-password-link'>forgot password</Link>
        </div>
        <div className='right-section-row'>
          <Link to='/signup' className='link signup-link'>
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
    </div>
  )
}

export default Signin
