import React from "react";
import "./NotFoundPage.css";
import { AddSEO } from "SEO";
import { NavLink } from "components";

const NotFoundPage: React.FC = (props) => {
  return (
    <div className="grid-start-2-end-2 not-found-page">
      <AddSEO
        title="404 - Page Not Found"
        description="The page you are looking for does not exist. Please check the URL or return to the homepage."
        keywords="404, not found, error, page missing"
      />
      <div className="not-found-card">
        <h2 className="not-found-title">404 - Page Not Found</h2>
        <p className="not-found-message">
          Sorry, the page you are looking for does not exist.
        </p>
        <NavLink to=".." type="link" icon="arrowBack">
          Return Back
        </NavLink>
      </div>
    </div>
  );
};

export default NotFoundPage;
