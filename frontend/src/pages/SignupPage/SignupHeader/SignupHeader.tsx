import React from 'react'
import './SignupHeader.css'
import { Link } from 'react-router-dom'
import { AppLogoImage } from 'components'
import { LazyIcon } from 'lazyUtils/LazyIcon/LazyIcon'

const SignupHeader: React.FC = (props) => {
  return (
    <div className='signup-header'>
      <div className='signup-header-info'>
        <AppLogoImage size={60} />
        <h3 className='form-label'>Sign up</h3>
        <p className='form-discription'>
          Join us by creating your account
        </p>
      </div>
      <Link to='../' className='link back-link'>
        <span className='icon'>
          <LazyIcon iconName='arrowBack' />
        </span>
        <span className='label'>Back</span>
      </Link>
    </div>
  )
}

export default SignupHeader
