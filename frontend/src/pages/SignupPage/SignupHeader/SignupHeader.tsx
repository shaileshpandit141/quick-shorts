import React from 'react'
import './SignupHeader.css'
import { AppLogoImage, NavLink } from 'components'

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
      <NavLink
        to='../'
        type='link'
        className='link back-link'
        iconName='arrowBack'
      >Back</NavLink>

    </div>
  )
}

export default SignupHeader
