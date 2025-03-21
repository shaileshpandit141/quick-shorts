import React from "react";
import "./Header.css";
import {
  AppLogo,
  Button,
  UserProfile,
  NavBarLinks,
  ToggleThemeButton,
  InstallAppButton,
} from "components";
import { useSidebar } from "context/features/SidebarProvider";

const Header: React.FC = () => {
  // Used sidebar hook to handle the sidebar action
  const { handleOpenSidebar } = useSidebar();

  return (
    <header className="inner-grid-1-1 grid-12 header">
      <div className="inner-grid-2-2 sub-headers">
        <div className="left-header">
          <Button
            type="icon"
            icon="menuOpen"
            title="open menu button"
            className="menu-open-button"
            onClick={handleOpenSidebar}
          />
          <AppLogo />
        </div>
        <div className="center-header">{/* Center TSX goes here */}</div>
        <div className="right-header">
          <NavBarLinks />
          <div className="other-links">
            <InstallAppButton />
            <ToggleThemeButton />
            <UserProfile />
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
