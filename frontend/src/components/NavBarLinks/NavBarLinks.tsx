import React from 'react';
import './NavBarLinks.css';
import { NavLink } from 'components'

const NavBarLinks: React.FC = () => {
  return (
    <nav className='nav-links'>
      <NavLink
        to='/home'
        type='link'
        className='link'
      >Home</NavLink>
    </nav>
  )
}

export default NavBarLinks;
