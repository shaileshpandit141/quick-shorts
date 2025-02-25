import React from "react";
import { NavLink } from "components";
import { isAuthenticated } from "utils";

const SigninLink: React.FC = (): JSX.Element | null => {
  if (isAuthenticated()) {
    return null;
  }

  return (
    <NavLink to="/auth/sign-in" type="link" icon="signin">
      Sign in
    </NavLink>
  );
};

export default SigninLink;
