import React, { useCallback, useMemo } from "react";
import "./GoogleSigninButton.css";
import { Navigate } from 'react-router-dom';
import { googleSigninUser } from "features/auth/signin";
import { GoogleLogin, GoogleOAuthProvider, CredentialResponse } from "@react-oauth/google";
import { getEnv, isAuthenticated } from "utils";

const GoogleSigninButton: React.FC = () => {
  const handleSuccess = useCallback(
    async (response: CredentialResponse) => {
      const authCode = response?.credential;
      if (authCode !== undefined) {
        await googleSigninUser({ token: authCode });
      } else {
        console.error("Google Sign-in failed! Please try again later.");
      }
    }, []);

  const handleFailure = useCallback(() => {
    console.error("Google Sign-in failed! Please try again later.");
  }, []);

  const clientId = useMemo(() => getEnv("GOOGLE_CLIENT_ID"), []);

  if (isAuthenticated()) {
    return <Navigate to="/home" />;
  }

  return (
    <GoogleOAuthProvider clientId={clientId}>
      <div className="google-button-wrapper">
        <GoogleLogin
          onSuccess={handleSuccess}
          onError={handleFailure}
          auto_select={false}
          cancel_on_tap_outside={false}
          theme="outline"
          size="large"
          shape="pill"
          logo_alignment="center"
        />
      </div>
    </GoogleOAuthProvider>
  );
};

export default GoogleSigninButton;
