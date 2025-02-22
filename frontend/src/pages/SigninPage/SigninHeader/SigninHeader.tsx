import React from 'react'
import './SigninHeader.css'
import { AppLogoImage, NavLink } from 'components'

const SigninHeader: React.FC = (props) => {
  return (
    <div className='signin-header'>
      <div className='signin-header-info'>
        <AppLogoImage size={60} />
        <h3 className='form-label'>Sign in</h3>
        <p className='form-discription'>
          Sign in with your existing credentials
        </p>
      </div>
      <NavLink
        to='../'
        type='link'
        className='link back-link'
        iconName='arrowBack'
      >Back</NavLink>
    </div>
  )
}

export default SigninHeader
