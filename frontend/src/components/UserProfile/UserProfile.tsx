import React, { useRef, useEffect } from "react";
import "./UserProfile.css";
import { Link } from "react-router-dom";
import { NavLink, SignoutButton } from "components";
import { useMenu } from "hooks";
import { user, useUserSelector } from "features/user";
import { isUserAuthenticated } from "utils/isUserAuthenticated";
import { getEnv } from "utils/getEnv";

const UserProfile: React.FC = (): JSX.Element | null => {
  const buttonRef = useRef(null);
  const userProfileRef = useRef(null);
  const { status, data } = useUserSelector();

  const { setVisibleStyle, setHiddenStyle } = useMenu({
    buttonRef: buttonRef,
    contentRef: userProfileRef,
  });

  useEffect(() => {
    setVisibleStyle((prevStyles) => ({
      ...prevStyles,
      transform: "scale(1)",
    }));

    setHiddenStyle((prevStyles) => ({
      ...prevStyles,
      transform: "scale(0.9)",
    }));
  }, [setVisibleStyle, setHiddenStyle]);

  useEffect(() => {
    if (status === "idle" && isUserAuthenticated()) {
      user();
    }
  }, [status]);

  if (!isUserAuthenticated() || status === "failed") {
    return null;
  }

  return (
    <div className="user-profile">
      <button className="button-as-icon profile-action-button" ref={buttonRef}>
        {"picture" in data && (
          <img src={data.picture} alt="user-picture-image" />
        )}
      </button>
      <div className="user-profile-card-container" ref={userProfileRef}>
        <div className="user-profile-header-card">
          <Link to="/dashboard" className="user-profile-container">
            <section className="user-profile-image">
              {"picture" in data && (
                <img src={data.picture} alt="user-picture-image" />
              )}
            </section>
            <section className="user-profile-info">
              <p className="email">{"email" in data && data.email}</p>
              <p className="view-settings">view dashboard</p>
            </section>
          </Link>
          <div className="line-break"></div>
          {"is_superuser" in data &&
            data.is_superuser &&
            "is_staff" in data &&
            data.is_staff && (
              <NavLink
                to={`${getEnv("BASE_API_URL")}/admin/`}
                type="link"
                className="edit-profile"
                target="_blank"
                icon="supervisorAccountIcon"
              >
                Django Admin
              </NavLink>
            )}
          <SignoutButton />
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
