import React, { FC, JSX } from "react";
import "./UserPage.css";

interface UserPageProps {}

const UserPage: FC<UserPageProps> = (props): JSX.Element => {
  return <div className="user-page">UserPage</div>;
};

export default UserPage;
