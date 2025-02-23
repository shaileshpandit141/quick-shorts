import { useEffect } from "react";
import { useLocation } from "react-router-dom";

export const useResetOnRouteChange = (resetFunction: () => void) => {
  const location = useLocation();

  useEffect(() => {
    return () => {
      resetFunction();
    };
  }, [location.pathname]);
};
