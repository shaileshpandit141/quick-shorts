import React from 'react'
import './Signin.css'
import { Link } from 'react-router-dom'
import AppLogo from 'components/common/appLogo/AppLogo'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'

const SigninWrapper: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className='signin-page'>
      <section className='left-section'>
        <AppLogo size={60} />
        <h3 className='form-label'>Sign in</h3>
        <p className='form-discription'>
          use your existing account
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

export default SigninWrapper
