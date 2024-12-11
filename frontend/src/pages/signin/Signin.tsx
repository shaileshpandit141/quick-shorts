import React from 'react'
import './Signin.css'
import { Link } from 'react-router-dom'
import AppLogo from 'components/common/appLogo/AppLogo'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'

const Signin: React.FC = (props) => {
  return (
    <div className='signin-page'>
      <section className='left-section'>
        <AppLogo size={60} />
        <h3 className='signin-label'>Sign in</h3>
        <p className='discription'>
          use your existing account
        </p>
        <Link to='../' className='link'>
          <span className='icon'>
            <LazyIconImport icon='arrowBack' />
          </span>
          <span className='label'>Back</span>
        </Link>
      </section>
      <section className='right-section'>
        right
      </section>
    </div>
  )
}

export default Signin
