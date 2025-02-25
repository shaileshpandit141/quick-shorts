import React from "react";
import "./Header.css";
import {
  AppLogo,
  UserProfile,
  NavBarLinks,
  ToggleThemeButton,
  InstallAppButton,
} from "components";
import SideBar from "components/SideBar/SideBar";

const Header: React.FC = (props) => {
  return (
    <header className="inner-grid-1-1 grid-12 header">
      <div className="inner-grid-2-2 sub-headers">
        <div className="left-header">
          <SideBar />
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
