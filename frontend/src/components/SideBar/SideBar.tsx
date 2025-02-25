import React, { useState } from "react";
import "./SideBar.css";
import {
  Drawer,
  NavBarLinks,
  Button,
  AppLogo,
  SigninLink,
  SignupLink,
} from "components";

const SideBar: React.FC = (): JSX.Element => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const handleMenuClick = (event: React.MouseEvent<HTMLElement>) => {
    event.preventDefault();
    setIsMenuOpen((prevState) => !prevState);
  };

  const sideBarClasses = isMenuOpen ? "side-bar--active" : "side-bar--inactive";

  return (
    <>
      <Button
        type="icon"
        icon="menuOpen"
        title="open menu button"
        className="menu-open-button"
        onClick={handleMenuClick}
      />
      <Drawer
        isOpen={isMenuOpen}
        onClick={handleMenuClick}
        className="side-bar-drawer"
      >
        <div className={`side-bar-container ${sideBarClasses}`}>
          <div className=" grid-12 side-bar-header">
            <div className="grid-start-2-end-2 header-buttons">
              <div className="header-buttons-left">
                <Button
                  type="icon"
                  icon="menuOpen"
                  title="close menu button"
                  className="close-menu-botton"
                  onClick={handleMenuClick}
                />
                <AppLogo />
              </div>
              <div className="header-buttons-right">
                {/* Right TSX Goes here */}
              </div>
            </div>
          </div>
          <div className="links-container">
            <div className="navbar-container">
              <NavBarLinks />
            </div>
            <div className="other-links-container">
              {/* Other TSX Links Goes here */}
              <SigninLink />
              <SignupLink />
            </div>
          </div>
        </div>
      </Drawer>
    </>
  );
};

export default SideBar;
