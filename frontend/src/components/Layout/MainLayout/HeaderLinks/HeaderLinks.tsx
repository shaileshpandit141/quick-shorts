import React from "react";
import "./HeaderLinks.css";
import { NavLink } from "components";

const HeaderLinks: React.FC = () => {
  return (
    <nav className="nav-links">
      <NavLink to="/home" type="link" className="link">
        Home
      </NavLink>
    </nav>
  );
};

export default HeaderLinks;
