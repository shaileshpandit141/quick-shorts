import React from "react";
import "./IndexPage.css";
import { isUserAuthenticated } from "utils/isUserAuthenticated";
import { Navigate } from "react-router-dom";

const IndexPageSkeleton: React.FC = () => {
  if (isUserAuthenticated()) {
    return <Navigate to={"/home"} />;
  }

  return (
    <div className="grid-12 index">
      <div className="grid-start-2-end-2 index-page">
        {/* Metadata settings */}
        <figure className="logo-container">
          <span className="img-skeleton skeleton"></span>
        </figure>
        <div className="heading-skeleton">
          <span className="skeleton"></span>
          <span className="skeleton"></span>
        </div>
        <p className="paragraph-skeleton">
          <span className="skeleton"></span>
          <span className="skeleton"></span>
        </p>
        <div className="buttons-skeleton">
          <span className="skeleton"></span>
          <span className="skeleton"></span>
        </div>
      </div>
    </div>
  );
};

export default IndexPageSkeleton;
