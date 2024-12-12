import React from 'react'
import './SignupHeader.css'
import { Link } from 'react-router-dom'
import AppLogo from 'components/common/appLogo/AppLogo'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'

const SignupHeader: React.FC = (props) => {
  return (
    <div className='signup-header'>
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
    </div>
  )
}

export default SignupHeader
