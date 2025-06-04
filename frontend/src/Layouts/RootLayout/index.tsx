import React from "react";
import "./RootLayout.css";
import { Outlet } from "react-router-dom";
import { ToastContainer, ToggleThemeButton } from "components";

const RootLayout: React.FC = () => {
  return (
    <div className="root-layout">
      <div className="global-theme-button-container">
        <ToggleThemeButton />
      </div>
      <ToastContainer />
      <Outlet />
    </div>
  );
};

export default RootLayout;
