import React from 'react'
import './SigninHeader.css'
import { Link } from 'react-router-dom'
import { AppLogo } from 'components'
import { LazyIcon } from 'lazyUtils/LazyIcon/LazyIcon'

const SigninHeader: React.FC = (props) => {
  return (
    <div className='signin-header'>
      <AppLogo size={60} />
      <h3 className='form-label'>Sign in</h3>
      <p className='-form-discription'>
        sign in with existing creadintials
      </p>
      <Link to='../' className='link back-link'>
        <span className='icon'>
          <LazyIcon iconName='arrowBack' />
        </span>
        <span className='label'>Back</span>
      </Link>
    </div>
  )
}

export default SigninHeader
