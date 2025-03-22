import React from "react";
import "./AppLogo.css";
import { Link } from "react-router-dom";
import { metaConfig } from "SEO";

const AppLogo: React.FC = () => {
  return (
    <Link to="/" className="app-logo">
      <figure className="logo-image-container">
        <img src="logo512.png" alt="logo-image" />
      </figure>
      <h4 className="logo-title">{metaConfig.appName}</h4>
    </Link>
  );
};

export default AppLogo;
