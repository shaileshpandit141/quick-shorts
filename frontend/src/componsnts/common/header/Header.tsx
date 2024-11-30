import React from 'react'
import './Header.css'
import { NavLink } from 'react-router-dom'

const Header: React.FC = (props) => {
  return (
    <div className='inner-grid-1-1 grid-12 header'>
      <div className='inner-grid-2-2 header-wrapper'>
        <NavLink to='/home'>Home</NavLink>
        <NavLink to='/signin'>Sign in</NavLink>
        <NavLink to='/signup'>Sign up</NavLink>
      </div>
    </div>
  )
}

export default Header
