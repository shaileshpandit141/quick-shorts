import React from "react";
import "./MainLayout.css";
import { Outlet } from "react-router-dom";
import { Header, Sidebar, Footer } from "components";

const MainLayout: React.FC = (props) => {
  return (
    <>
      <Sidebar />
      <section className="inner-grid-1-1 grid-12 header-wrapper">
        <Header />
      </section>
      <main className="inner-grid-1-1 grid-12 main-content">
        <Outlet />
      </main>
      <section className="inner-grid-1-1 grid-12">
        <Footer />
      </section>
    </>
  );
};

export default MainLayout;
