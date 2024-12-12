import React from 'react'
import './Signup.css'
import { Link } from 'react-router-dom'
import AppLogo from 'components/common/appLogo/AppLogo'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'

const SignupWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className='signup-page'>
      <section className='left-section'>
        <AppLogo size={60} />
        <h3 className='form-label'>Sign up</h3>
        <p className='-form-discription'>
          create an new account
        </p>
        <Link to='../' className='link back-link'>
          <span className='icon'>
            <LazyIconImport icon='arrowBack' />
          </span>
          <span className='label'>Back</span>
        </Link>
      </section>
      <section className='right-section'>
        {children}
      </section>
    </div>
  )
}

export default SignupWrapper
