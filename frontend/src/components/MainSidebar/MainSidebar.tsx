import React, { useEffect } from "react";
import "./MainSidebar.css";
import { useLocation } from "react-router-dom";
import {
  Drawer,
  HeaderLinks,
  Button,
  AppLogo,
  SigninLink,
  SignupLink,
} from "components";
import { useMainSidebar } from "context/features/MainSidebarProvider";

const MainSidebar: React.FC = (): JSX.Element => {
  const location = useLocation();

  // Used sidebar hook to handle the sidebar action
  const { isSidebarOpen, handleCloseSidebar } = useMainSidebar();

  // Change the sidebar classes base on sidebar state
  const sideBarClasses = isSidebarOpen
    ? "side-bar--active"
    : "side-bar--inactive";

  // Hnadle sidebar close if route is change
  useEffect(() => {
    handleCloseSidebar();
  }, [location]);

  return (
    <Drawer
      isOpen={isSidebarOpen}
      onClick={handleCloseSidebar}
      className="side-bar-drawer"
    >
      <div className={`side-bar-container ${sideBarClasses}`}>
        <div className=" grid-12 side-bar-header">
          <div className="grid-start-2-end-2 header-buttons">
            <div className="header-buttons-left">
              <Button
                type="icon"
                icon="sidebarIcon"
                title="close menu button"
                className="close-menu-botton"
                onClick={handleCloseSidebar}
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
            <HeaderLinks />
          </div>
          <div className="other-links-container">
            {/* Other TSX Links Goes here */}
            <SigninLink />
            <SignupLink />
          </div>
        </div>
      </div>
    </Drawer>
  );
};

export default MainSidebar;
