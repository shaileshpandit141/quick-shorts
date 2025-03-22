import React, { JSX } from "react";
import "./DashboardSidebar.css";
import { AppLogo, NavLink, Button } from "components";
import { useDashboardSmaillSidebar } from "context/features/DashboardSmaillSidebarProvider"

const DashboardSidebar: React.FC = (): JSX.Element => {
  // Used dashboard small sidebar hook to handle the sidebar action
  const { handleCloseSidebar } = useDashboardSmaillSidebar();

  return (
    <div className="dashboard-sidebar">
      <div className="grid-12 header-container">
        <div className="grid-start-2-end-2 header-container-wrapper">
          <Button
            type="icon"
            icon="sidebarIcon"
            title="close dashboard sidebar button"
            className="close-dashboard-sidebar-button"
            onClick={handleCloseSidebar}
          />
          <AppLogo />
        </div>
      </div>
      <div className="grid-12 nav-links-container">
        <div className="grid-start-2-end-2 nav-links-container-wrapper">
          <NavLink to="." type="link" icon="dashboardIcon">dashboard</NavLink>
          <NavLink to="profile" type="link" icon="person">profile</NavLink>
        </div>
      </div>
    </div>
  )
}

export default DashboardSidebar;
