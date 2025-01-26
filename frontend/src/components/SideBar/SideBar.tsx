import React, { useState } from 'react';
import './SideBar.css';
import { Drawer, NavBar, Button, ToggleThemeButton } from 'components';

const SideBar: React.FC = (): JSX.Element => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>) => {
    event.preventDefault()
    setIsMenuOpen(prevState => !prevState);
  };

  return (
    <>
      <Button
        type='icon'
        iconName='menuOpen'
        title='open menu button'
        className='menu-open-button'
        onClick={handleMenuClick}
      />
      <Drawer
        isOpen={isMenuOpen}
        onClick={handleMenuClick}
        className='side-bar-drawer'
      >
        <div className={`side-bar-container ${isMenuOpen ? 'side-bar--active' : 'side-bar--inactive'}`}>
          <div className=' grid-12 side-bar-header'>
            <div className='grid-start-2-end-2 header-buttons'>
              <div className='header-buttons-left'>
                {/* <AppLogo /> */}
                {/* <h4>React</h4> */}
              </div>
              <div className='header-buttons-right'>
                <ToggleThemeButton />
                <Button
                  type='icon'
                  iconName='close'
                  title='close menu button'
                  onClick={handleMenuClick}
                />
              </div>
            </div>
          </div>
          <div className=' grid-12 header-navbar'>
            <div className='grid-start-2-end-2 navbar'>
              <NavBar />
            </div>
          </div>
        </div>
      </Drawer>
    </>
  )
}

export default SideBar;
