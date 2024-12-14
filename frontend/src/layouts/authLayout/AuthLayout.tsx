import React from 'react'
import './AuthLayout.css'
import { Outlet } from 'react-router-dom'
import { ToggleThemeButton } from 'components'

const AuthLayout: React.FC = (props) => {
  return (
    <div className='inner-grid-1-1 auth-alyout'>
      <div className='grid-12 theme-button-wrapper'>
        <div className='inner-grid-2-2 theme-button-container'>
          <ToggleThemeButton />
        </div>
      </div>
      <div className='form-wrapper'>
        <Outlet />
      </div>
    </div>
  )
}

export default AuthLayout
