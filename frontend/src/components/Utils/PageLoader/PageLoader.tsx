import React from "react";
import "./PageLoader.css";
import { Loader } from "components";

const PageLoader: React.FC = () => {
  return (
    <div className="page-loader">
      <div className="icon-container">
        <Loader />
      </div>
    </div>
  );
};

export default PageLoader;
