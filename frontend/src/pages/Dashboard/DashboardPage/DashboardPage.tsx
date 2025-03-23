import React, { FC, JSX } from "react";
import "./DashboardPage.css";
import { AddSEO } from "SEO";

interface DashboardPageProps {}

const DashboardPage: FC<DashboardPageProps> = (props): JSX.Element => {
  return (
    <div className="dashboard-page">
      <AddSEO title="Dashboard" description="" />
      <h2>Lorem ipsum dolor sit amet.</h2>
      <p>
        Lorem ipsum dolor sit amet consectetur adipisicing elit. Modi voluptas
        libero recusandae necessitatibus architecto delectus mollitia! Numquam
        fugiat a inventore, alias reprehenderit tempora omnis dolore optio nobis
        ducimus. Fugit, eveniet.
      </p>
    </div>
  );
};

export default DashboardPage;
