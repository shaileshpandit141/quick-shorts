import React, { useEffect } from "react";
import "./VerifyUserAccountPage.css";
import { useParams } from "react-router-dom";
import { useResetOnRouteChange } from "hooks";
import { NavLink, Button, DisplayFormErrors, SigninLink } from "components";
import {
  useVerifyUserAccountSelector,
  verifyUserAccount,
  resetVerifyUserAccount,
} from "features/auth/verifyUserAccount";
import { triggerToast } from "features/toast";

const VerifyUserAccountPage: React.FC = (): JSX.Element => {
  const { token } = useParams<{ token: string }>();
  const { status, message, errors, data } = useVerifyUserAccountSelector();

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    verifyUserAccount({
      token: token || "",
    });
  };

  useEffect(() => {
    if (status === "succeeded") {
      triggerToast("success", message);
    } else if (status === "failed") {
      triggerToast("error", message);
    }
  }, [message, status]);

  useResetOnRouteChange(() => {
    resetVerifyUserAccount();
  });

  return (
    <div className="verify-user-account-page">
      <div className="header">
        <h3 className="form-label">Verify your account</h3>
        <p className="form-description">
          Click the Verify button below to verify your account.
        </p>
      </div>
      <form className="form" onSubmit={handleSubmit}>
        <DisplayFormErrors field={"none"} errors={errors} />
        <DisplayFormErrors field={"token"} errors={errors} />
        {data?.detail && <p>{data.detail}</p>}
        <div className="actions">
          <NavLink
            to="../../"
            type="link"
            className="link back-link"
            icon="arrowBack"
          >
            Back
          </NavLink>
          <Button
            type="submit"
            icon={status === "succeeded" ? "checkCircle" : "click"}
            className="button"
            isLoaderOn={status === "loading"}
            isDisabled={status === "succeeded"}
          >
            Verify
          </Button>
        </div>
        {status === "succeeded" && <SigninLink />}
      </form>
    </div>
  );
};

export default VerifyUserAccountPage;
