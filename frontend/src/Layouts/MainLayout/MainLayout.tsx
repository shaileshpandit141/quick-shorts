import React from "react";
import "./MainLayout.css";
import { Outlet } from "react-router-dom";
import { Header, Sidebar, Footer } from "components";

const MainLayout: React.FC = () => {
  return (
    <div className="main-layout">
      <Sidebar />
      <div className="main-layout-continer">
        <section className="main-layout-header">
          <Header />
        </section>
        <section className="main-layout-content-container">
          <main className="main-layout-content">
            <Outlet />
          </main>
          <footer className="main-layout-footer">
            <Footer />
          </footer>
        </section>
      </div>
    </div>
  );
};

export default MainLayout;
