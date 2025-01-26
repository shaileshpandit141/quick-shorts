import React from 'react'
import './Header.css'
import { Link } from 'react-router-dom'
import { AppLogo, Profile } from 'components'
import NavBar from 'components/NavBar/NavBar'
import ToggleThemeButton from 'components/ToggleThemeButton/ToggleThemeButton'
import InstallAppButton from 'components/InstallAppButton/InstallAppButton'
import SignoutButton from 'components/SignoutButton/SignoutButton'
import SideBar from 'components/SideBar/SideBar'

const Header: React.FC = (props) => {
  return (
    <header className='inner-grid-1-1 grid-12 header'>
      <div className='inner-grid-2-2 sub-headers'>
        <div className='left-header'>
          <Link to='/' className='left-header-link'>
            <AppLogo />
            <h4>React</h4>
          </Link>
        </div>
        <div className='center-header'>
          {/* Center TSX goes here */}
        </div>
        <div className='right-header'>
          <NavBar />
          <div className='other-links'>
            <SignoutButton />
            <InstallAppButton />
            <ToggleThemeButton />
            <SideBar />
            <Profile />
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
