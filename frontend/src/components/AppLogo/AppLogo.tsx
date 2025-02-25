import React from "react";
import "./AppLogo.css";
import { Link } from "react-router-dom";
import { AppLogoImage } from "components";
import { metaConfig } from "SEO";

const AppLogo: React.FC = () => {
  return (
    <Link to="/" className="app-logo">
      <AppLogoImage />
      <h4 className="logo-title">{metaConfig.appName}</h4>
    </Link>
  );
};

export default AppLogo;
