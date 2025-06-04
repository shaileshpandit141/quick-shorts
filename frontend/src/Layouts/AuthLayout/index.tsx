import React from "react";
import "./AuthLayout.css";
import { Outlet } from "react-router-dom";

const AuthLayout: React.FC = (props) => {
  return (
    <div className="auth-layout">
      <Outlet />
    </div>
  );
};

export default AuthLayout;
