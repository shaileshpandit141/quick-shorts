import React from 'react'
import './AuthLayout.css'
import { Outlet } from 'react-router-dom'

const AuthLayout: React.FC = (props) => {
  return (
    <div className='inner-grid-1-1 auth-alyout'>
      <Outlet />
    </div>
  )
}

export default AuthLayout
