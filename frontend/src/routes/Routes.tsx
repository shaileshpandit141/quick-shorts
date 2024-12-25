// Named Imports (external libraries).
import React from 'react'
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom'
import { lazyModuleImport, LazyModuleLoader } from 'lazyUtils/lazyModuleImport'

// Default Imports (user-defined layout and pages).
import PrivateRoute from './PrivateRoute'
import PublicRoute from './PublicRoute'
import MainLayout from 'layouts//MainLayout/MainLayout'
import AuthLayout from 'layouts/AuthLayout/AuthLayout'

// Default Page loader Imports
import { PageLoader } from 'components'
import IndexPageSkeleton from 'pages/IndexPage/IndexPageSkeleton'

const IndexPage = lazyModuleImport(() => import('pages/IndexPage/IndexPage'))
const Home = lazyModuleImport(() => import('pages/home/Home'))
const SigninPage = lazyModuleImport(() => import('pages/SigninPage/SigninPage'))
const SignupPage = lazyModuleImport(() => import('pages/SignupPage/SignupPage'))
const NotFound = lazyModuleImport(() => import('pages/NotFound/NotFound'))

const AppRoutes: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route element={<MainLayout />}>

          {/* Public Routes */}
          <Route element={<PublicRoute />}>
            <Route index element={
              <LazyModuleLoader element={<IndexPage />} fallback={<IndexPageSkeleton />} />
            } />
          </Route>

          {/* Private Routes */}
          <Route element={<PrivateRoute />}>
            <Route path='/home' element={
              <LazyModuleLoader element={<Home />} fallback={<PageLoader />} />
            } />
          </Route>
        </Route>

        {/* Auth Routes without header */}
        <Route element={<AuthLayout />}>
          <Route path='/sign-in' element={
            <LazyModuleLoader element={<SigninPage />} fallback={<PageLoader />} />
          } />
          <Route path='/sign-up' element={
            <LazyModuleLoader element={<SignupPage />} fallback={<PageLoader />} />
          } />
        </Route>

        {/* Catch-all route for 404 Not Found */}
        <Route path="*" element={
          <LazyModuleLoader element={<NotFound />} fallback={<PageLoader />} />
        } />
      </Routes>
    </Router>
  )
}

export default AppRoutes
