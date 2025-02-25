import React from "react";
import "./IndexPage.css";
import { Navigate } from "react-router-dom";
import { AddSEO } from "SEO";
import { isAuthenticated } from "utils";
import { SigninLink, SignupLink } from "components";

const IndexPage: React.FC = (props) => {
  if (isAuthenticated()) {
    return <Navigate to={"/home"} />;
  }
  return (
    <div className="inner-grid-1-1 grid-12 index">
      <AddSEO
        title="Index"
        description="Welcome to my website, where you can find the best content."
        keywords="home, react, SEO, optimization"
      />
      <div className="inner-grid-2-2 index-page">
        {/* Metadata settings */}
        <figure className="logo-container">
          <img src="logo512.png" alt="logo512.png" />
        </figure>
        <h1>Welcome to building robust UI's</h1>
        <p>
          This boilerplate includes all the necessary setup for building robust
          UI's using React With Django and Django Rest Framework.
        </p>
        <div className="buttons-conatiner">
          <SigninLink />
          <SignupLink />
        </div>
      </div>
    </div>
  );
};

export default IndexPage;
