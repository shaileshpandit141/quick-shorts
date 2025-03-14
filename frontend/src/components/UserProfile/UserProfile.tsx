import React, { useRef, useEffect } from "react";
import "./UserProfile.css";
import { NavLink, SignoutButton } from "components";
import { useMenu } from "hooks";
import { user, useUserSelector } from "features/user";
import { isUserAuthenticated } from "utils/isUserAuthenticated";
import { buildMediaURL } from "utils/buildMediaURL";
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

  if (!isUserAuthenticated() || (status === "failed")) {
    return null;
  }

  return (
    <div className="user-profile">
      <button className="button-as-icon profile-action-button" ref={buttonRef}>
        {("avatar" in data) && (
          <img src={buildMediaURL(data.avatar)} alt="avatar-image" />
        )}
      </button>
      <div className="user-profile-card-container" ref={userProfileRef}>
        <div className="user-profile-header-card">
          <section className="user-profile-image">
            {("avatar" in data) && (
              <img src={buildMediaURL(data.avatar)} alt="avatar-image" />
            )}
          </section>
          <section className="user-profile-info">
            <p className="username">{("username" in data) && data.username}</p>
            <p className="email">{("email" in data) && data.email}</p>
          </section>
          {((("is_superuser" in data) && data.is_superuser)
            && (("is_staff" in data) && data.is_staff)) && (
              <NavLink
                to={`${getEnv("BASE_API_URL")}/admin/`}
                type="link"
                className="edit-profile"
                target="_blank"
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
