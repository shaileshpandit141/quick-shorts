import React from 'react';
import './NavBar.css';
import { NavLink } from 'react-router-dom'
import { isAuthenticated } from 'features/auth'
import AnchorLink from 'components/AnchorLink/AnchorLink'

const NavBar: React.FC = () => {
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

export default NavBar;
