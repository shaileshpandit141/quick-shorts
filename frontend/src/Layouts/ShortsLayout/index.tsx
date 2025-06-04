import React, { FC, JSX } from "react";
import "./ShortsLayout.css";
import { Outlet } from "react-router-dom";
import { NavLink } from "components";

interface ShortsLayoutProps {}

const ShortsLayout: FC<ShortsLayoutProps> = (props): JSX.Element => {
  return (
    <div className="shorts-layout">
      <div className="shorts-layout-wrapper">
        <div className="outlet-container">
          <Outlet />
        </div>
        <div className="tab-navigation-container">
          <NavLink to="/user" type="link">
            Username
          </NavLink>
          <NavLink to="/" type="link">
            Shorts
          </NavLink>
          <NavLink to="/shorts-create" type="link">
            Create
          </NavLink>
        </div>
      </div>
    </div>
  );
};

export default ShortsLayout;
