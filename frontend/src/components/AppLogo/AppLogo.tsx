import React from 'react'
import './AppLogo.css'
import { Link } from 'react-router-dom'
import { AppLogoImage } from 'components';

const AppLogo: React.FC = () => {

  return (
    <Link to='/' className='app-logo'>
      <AppLogoImage />
      <h4 className='logo-title'>React</h4>
    </Link>
  )
}

export default AppLogo;
