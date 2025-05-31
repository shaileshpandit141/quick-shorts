import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { importLazyModule, RenderLazyModule } from "lazyUtils";

// Default Imports (user-defined layout and pages).
import { PrivateRoute, PublicRoute } from "./RoutesPrivacy";
import { RootLayout, MainLayout, AuthLayout } from "Layouts";
import ShortsLayout from "Layouts/ShortsLayout";

// Default Page loader Imports
import { PageLoader } from "components";
import IndexPageSkeleton from "pages/IndexPage";

// Lazy-loaded Page Imports
const IndexPage = importLazyModule(() => import("pages/IndexPage"));
const HomePage = importLazyModule(() => import("pages/HomePage"));
const SigninPage = importLazyModule(() => import("pages/SigninPage"));
const SignupPage = importLazyModule(() => import("pages/SignupPage"));
const VerifyUserAccountPage = importLazyModule(
  () => import("pages/VerifyUserAccountPage"),
);

// Shorts page import
const Shorts = importLazyModule(() => import("pages/Shorts/Shorts"));

// Lazy-loaded 404 Not Found Page
const NotFoundPage = importLazyModule(() => import("pages/NotFoundPage"));

const AppRoutes: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<RootLayout />}>
          {/* Routes with header and Footer */}
          {/* ----------------------------- */}
          <Route element={<MainLayout />}>
            {/* Private Routes with header and Footer */}
            <Route element={<PrivateRoute />}>
              <Route
                path="/home"
                element={
                  <RenderLazyModule
                    element={<HomePage />}
                    fallback={<PageLoader />}
                  />
                }
              />
            </Route>

            {/* Public Routes with header and Footer */}
            <Route element={<PublicRoute />}>
              <Route
                index
                element={
                  <RenderLazyModule
                    element={<IndexPage />}
                    fallback={<IndexPageSkeleton />}
                  />
                }
              />
              {/* <Route
                path="shorts"
                element={
                  <RenderLazyModule
                    element={<Shorts />}
                    fallback={<PageLoader />}
                  />
                }
              /> */}
            </Route>
          </Route>

          {/* Routes without header and Footer */}
          {/* -------------------------------- */}
          <Route>
            {/* Private Routes without header and Footer */}
            <Route element={<PrivateRoute />}></Route>

            {/* Public Routes without header and Footer */}
            <Route element={<PublicRoute />}>

              <Route path="/shorts" element={<ShortsLayout />}>
                <Route
                  index
                  element={
                    <RenderLazyModule
                      element={<Shorts />}
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
