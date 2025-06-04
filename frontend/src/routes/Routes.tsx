import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { importLazyModule, RenderLazyModule } from "lazyUtils";

// Default Imports (user-defined layout and pages).
import { PrivateRoute, PublicRoute } from "./RoutesPrivacy";
import RootLayout from "Layouts/RootLayout";
import AuthLayout from "Layouts/AuthLayout";
import ShortsLayout from "Layouts/ShortsLayout";

// Default Page loader Imports
import { PageLoader } from "components";

// Lazy-loaded Page Imports
const SigninPage = importLazyModule(() => import("pages/SigninPage"));
const SignupPage = importLazyModule(() => import("pages/SignupPage"));
const VerifyUserAccountPage = importLazyModule(
  () => import("pages/VerifyUserAccountPage"),
);
const ShortsPage = importLazyModule(() => import("pages/ShortsPage"));
const UserPage = importLazyModule(() => import("pages/UserPage"));
const ShortsCreatePage = importLazyModule(
  () => import("pages/ShortsCreatePage"),
);

// Lazy-loaded 404 Not Found Page
const NotFoundPage = importLazyModule(() => import("pages/NotFoundPage"));

const AppRoutes: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<RootLayout />}>
          <Route>
            {/* Private Routes without header and Footer */}
            <Route element={<PrivateRoute />}></Route>

            {/* Public Routes without header and Footer */}
            <Route element={<PublicRoute />}>
              <Route element={<ShortsLayout />}>
                <Route
                  index
                  element={
                    <RenderLazyModule
                      element={<ShortsPage />}
                      fallback={<PageLoader />}
                    />
                  }
                />
                <Route
                  path="/user"
                  element={
                    <RenderLazyModule
                      element={<UserPage />}
                      fallback={<PageLoader />}
                    />
                  }
                />
                <Route
                  path="/shorts-create"
                  element={
                    <RenderLazyModule
                      element={<ShortsCreatePage />}
                      fallback={<PageLoader />}
                    />
                  }
                />
              </Route>

              <Route element={<AuthLayout />}>
                <Route
                  path="sign-in"
                  element={
                    <RenderLazyModule
                      element={<SigninPage />}
                      fallback={<PageLoader />}
                    />
                  }
                />
                <Route
                  path="sign-up"
                  element={
                    <RenderLazyModule
                      element={<SignupPage />}
                      fallback={<PageLoader />}
                    />
                  }
                />
                <Route
                  path="verify-user-account/:token"
                  element={
                    <RenderLazyModule
                      element={<VerifyUserAccountPage />}
                      fallback={<PageLoader />}
                    />
                  }
                />
              </Route>
            </Route>
          </Route>

          {/* Catch-all route for 404 Not Found Page */}
          {/* -------------------------------------- */}
          <Route
            path="*"
            element={
              <RenderLazyModule
                element={<NotFoundPage />}
                fallback={<PageLoader />}
              />
            }
          />
        </Route>
      </Routes>
    </Router>
  );
};

export default AppRoutes;
