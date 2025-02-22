import React from "react";
import { NavLink } from 'components';
import { isAuthenticated } from "utils";

const SigninLink: React.FC = (): JSX.Element | null => {
  if (isAuthenticated()) {
    return null;
  }

  return (
    <NavLink
      to='/sign-in'
      type='link'
      iconName='signin'
    >
      Sign in
    </NavLink>
  )
}

export default SigninLink;
