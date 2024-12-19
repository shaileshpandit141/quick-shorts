import React from 'react'
import './RightHeader.css'
import { NavLink } from 'react-router-dom'
import { SigninLink } from 'components'
import { SignupLink } from 'components'
import { ToggleThemeButton } from 'components'

const RightHeader: React.FC = (props) => {
  return (
    <div className='right-header'>
      <NavLink to='/home' className='link'>Home</NavLink>
      <SigninLink />
      <SignupLink />
      <ToggleThemeButton />
    </div>
  )
}

export default RightHeader
