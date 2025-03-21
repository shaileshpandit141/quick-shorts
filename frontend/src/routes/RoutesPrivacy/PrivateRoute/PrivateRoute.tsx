import { useEffect, useState } from "react";
import { Navigate, Outlet } from "react-router-dom";
import { useSigninUserSelector, resetSigninUser } from "features/auth/signin";
import { JWTTokenHandler } from "utils/JWTTokenHandler";

const PrivateRoute = (): JSX.Element => {
  const { data } = useSigninUserSelector();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(true);

  useEffect(() => {
    const tokenHandler = new JWTTokenHandler(data.refresh_token || "");
    if (!data.refresh_token || tokenHandler.isTokenExpired()) {
      resetSigninUser();
      setIsAuthenticated(false);
    } else {
      setIsAuthenticated(true);
    }
  }, [data]);

  return isAuthenticated ? (
    <Outlet />
  ) : (
    <Navigate to="/sign-in" replace={true} />
  );
};

export default PrivateRoute;
