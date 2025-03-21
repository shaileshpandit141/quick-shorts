import React from "react";
import { NavLink } from "components";
import { isUserAuthenticated } from "utils/isUserAuthenticated";

const SignupLink: React.FC = (): JSX.Element | null => {
  if (isUserAuthenticated()) {
    return null;
  }

  return (
    <NavLink to="/sign-up" type="link" icon="signup">
      Sign up
    </NavLink>
  );
};

export default SignupLink;
