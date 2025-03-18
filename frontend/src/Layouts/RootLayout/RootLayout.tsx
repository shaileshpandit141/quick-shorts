import React from "react";
import "./RootLayout.css";
import { Outlet } from "react-router-dom";
import { ToastContainer, ToggleThemeButton, Sidebar } from "components";

const RootLayout: React.FC = () => {
  return (
    <>
      <div className="global-theme-button-container">
        <ToggleThemeButton />
      </div>
      <Sidebar />
      <ToastContainer />
      <Outlet />
    </>
  );
};

export default RootLayout;
