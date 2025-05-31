import React, { FC, JSX } from "react";
import "./ShortsLayout.css";
import { Outlet } from "react-router-dom";
import { NavLink } from "components";
import ActionButtons from "components/Pages/Shorts/ActionButtons";

interface ShortsLayoutProps {}

const ShortsLayout: FC<ShortsLayoutProps> = (props): JSX.Element => {
  return (
    <div className="shorts-layout">
      <div className="shorts-layout-wrapper">
        <div className="outlet-container">
          <Outlet />
        </div>
        <div className="shorts-header">
          <NavLink to="/user" type="link">
            Username
          </NavLink>
          <NavLink to="/shorts" type="link">
            Shorts
          </NavLink>
          <NavLink to="/create" type="link">
            Create
          </NavLink>
        </div>
      </div>
      <div className="action-btns-container">
        <div>
          <ActionButtons />
        </div>
      </div>
    </div>
  );
};

export default ShortsLayout;
