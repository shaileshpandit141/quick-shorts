import React from 'react'
import './AuthLayout.css'
import { Outlet } from 'react-router-dom'
import ToggleThemeButton from 'components/common/header/toggleThemeButton/ToggleThemeButton'

const AuthLayout: React.FC = (props) => {
  return (
    <div className='inner-grid-1-1 auth-alyout'>
      <div className='theme-button-container'>
        <ToggleThemeButton />
      </div>
      <div className='form-wrapper'>
        <Outlet />
      </div>
    </div>
  )
}

export default AuthLayout
