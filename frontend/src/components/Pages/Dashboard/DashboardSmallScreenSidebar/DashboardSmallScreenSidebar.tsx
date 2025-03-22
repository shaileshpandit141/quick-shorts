import React, { JSX, useEffect } from "react";
import "./DashboardSmallScreenSidebar.css";
import { useLocation } from "react-router-dom";
import { Drawer, DashboardSidebar } from "components";
import { useDashboardSmaillSidebar } from "context/features/DashboardSmaillSidebarProvider";

const DashboardSmallScreenSidebar: React.FC = (): JSX.Element => {
  const location = useLocation();

  // Used dashboard small sidebar hook to handle the sidebar action
  const { isSidebarOpen, handleCloseSidebar } = useDashboardSmaillSidebar();

  // Change the sidebar classes base on sidebar state
  const sideBarClasses = isSidebarOpen
    ? "side-bar--active"
    : "side-bar--inactive";

  // Hnadle sidebar close if route is change
  useEffect(() => {
    handleCloseSidebar();
  }, [location]);

  return (
    <Drawer
      isOpen={isSidebarOpen}
      onClick={handleCloseSidebar}
      className="dashboard-small-screen-sidebar-drawer"
    >
      <div className={`dashboard-small-screen-sidebar ${sideBarClasses}`}>
        <DashboardSidebar />
      </div>
    </Drawer>
  )
}

export default DashboardSmallScreenSidebar;
