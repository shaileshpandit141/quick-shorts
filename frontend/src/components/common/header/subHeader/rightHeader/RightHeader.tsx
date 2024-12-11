import React from 'react'
import './RightHeader.css'
import { NavLink } from 'react-router-dom'
import ToggleThemeButton from '../../toggleThemeButton/ToggleThemeButton'

const RightHeader: React.FC = (props) => {
  return (
    <div className='right-header'>
      <NavLink to='/home' className='link'>Home</NavLink>
      <NavLink to='/signin' className='link'>Sign in</NavLink>
      <NavLink to='/signup' className='link'>Sign up</NavLink>
      <ToggleThemeButton />
    </div>
  )
}

export default RightHeader
