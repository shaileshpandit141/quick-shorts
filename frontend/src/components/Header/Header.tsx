import React from 'react'
import './Header.css'
import LeftHeader from './SubHeader/LeftHeader/LeftHeader'
import CenterHeader from './SubHeader/CenterHeader/CenterHeader'
import RightHeader from './SubHeader/RightHeader/RightHeader'
import ToggleThemeButton from 'components/ToggleThemeButton/ToggleThemeButton'
import InstallAppButton from 'components/InstallAppButton/InstallAppButton'
import SignoutButton from 'components/SignoutButton/SignoutButton'

const Header: React.FC = (props) => {
  return (
    <header className='inner-grid-1-1 grid-12 header'>
      <div className='inner-grid-2-2 sub-headers'>
        <div className='left-header'>
          <LeftHeader />
        </div>
        <div className='center-header'>
          <CenterHeader />
        </div>
        <div className='right-header'>
          <RightHeader />
          <div className='other-links'>
            <SignoutButton />
            <InstallAppButton />
            <ToggleThemeButton />
          </div>
        </div>
      </div>
    </header>
  )
}

export default Header
