import React from "react";
import "./Footer.css";
import { Link } from "react-router-dom";
import { metaConfig } from "SEO";

const Footer: React.FC = (props) => {
  const copyRightYear = new Date().getFullYear();

  return (
    <footer className="grid-12 footer">
      <div className="grid-start-2-end-2 footer-wrapper">
        <div className="content">
          {/* Footer TSX content goes here */}
          Footer
        </div>
        <section className="copy-right-container">
          <p className="copy-right-text">
            &copy; {copyRightYear} {metaConfig.appName}. All rights reserved.
            &#124;{" "}
            <Link to="/privacy-policy" className="links">
              Privacy Policy
            </Link>{" "}
            &#124;{" "}
            <Link to="/terms" className="links">
              Terms of Service
            </Link>
          </p>
        </section>
      </div>
    </footer>
  );
};

export default Footer;
