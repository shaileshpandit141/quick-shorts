import React from 'react'
import './RightHeader.css'
import { NavLink } from 'react-router-dom'
import { isAuthenticated } from 'utils/isAuthenticted'
import { ToggleThemeButton } from 'components'
import { AnchorLink } from 'components'
import { InstallAppButton } from 'components'

const RightHeader: React.FC = (props) => {
  return (
    <div className='right-header'>
      <NavLink to='/home' className='link'>Home</NavLink>
      {isAuthenticated() ? null : (
        <AnchorLink to="sign-in" type="link">sign in</AnchorLink>
      )}
      {isAuthenticated() ? null : (
        <AnchorLink to="sign-up" type="link">sign up</AnchorLink>
      )}
      <ToggleThemeButton />
      <InstallAppButton />
    </div>
  )
}

export default RightHeader
