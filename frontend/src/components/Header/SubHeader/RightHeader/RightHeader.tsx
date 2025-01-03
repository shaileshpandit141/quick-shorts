import React from 'react'
import './RightHeader.css'
import { NavLink } from 'react-router-dom'
import { isAuthenticated } from 'utils/isAuthenticted'
import AnchorLink from 'components/AnchorLink/AnchorLink'

const RightHeader: React.FC = (props) => {
  return (
    <nav className='nav-links'>
      <NavLink to='/home' className='link'>Home</NavLink>
      {isAuthenticated() ? null : (
        <AnchorLink to="sign-in" type="link">sign in</AnchorLink>
      )}
      {isAuthenticated() ? null : (
        <AnchorLink to="sign-up" type="link">sign up</AnchorLink>
      )}
    </nav>
  )
}

export default RightHeader
