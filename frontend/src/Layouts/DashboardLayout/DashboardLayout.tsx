import React, { JSX } from "react";
import "./DashboardLayout.css";
import { Outlet } from "react-router-dom";
import {
  DashboardSidebar,
  DashboardHeader,
  DashboardSmallScreenSidebar,
} from "components";

const DashboardLayout: React.FC = (): JSX.Element => {
  return (
    <div className="dashboard-layout">
      <DashboardSmallScreenSidebar />
      <section className="grid-12 left-grid">
        <div className="grid-start-1-end-1 left-grid-wrapper">
          <DashboardSidebar />
        </div>
      </section>
      <section className="grid-12 right-grid">
        <div className="grid-start-1-end-1 right-grid-wrapper">
          <div className="dashboard-containt-container">
            {/* Dashboard containt header TSX */}
            <header className="grid-12 dashboard-containt-header">
              <header className="grid-start-2-end-2 dashboard-containt-header-wrapper">
                <DashboardHeader />
              </header>
            </header>
            {/* Dashboard containt TSX */}
            <div className="grid-12 dashboard-content">
              <div className="grid-start-2-end-2 dashboard-content-wrapper">
                <Outlet />
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default DashboardLayout;
