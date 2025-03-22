import React, { JSX } from "react";
import "./DashboardHeader.css";
import { ToggleThemeButton, UserProfile, Button, AppLogo } from "components";
import { useDashboardSmaillSidebar } from "context/features/DashboardSmaillSidebarProvider"

const DashboardHeader: React.FC = (): JSX.Element => {
  // Used dashboard small sidebar hook to handle the sidebar action
  const { handleOpenSidebar } = useDashboardSmaillSidebar();

  return (
    <header className="dashboard-header">
      <section className="left-header-grid">
        <div className="conditional-elements">
          <Button
            type="icon"
            icon="sidebarIcon"
            title="open dashboard sidebar button"
            className="open-dashboard-sidebar-button"
            onClick={handleOpenSidebar}
          />
          <AppLogo />
        </div>
      </section>
      <section className="right-header-grid">
        <ToggleThemeButton />
        <UserProfile />
      </section>
    </header>
  )
}

export default DashboardHeader;
