// Named Imports (external libraries).
import React from 'react'
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom'
import { lazyModuleImport, LazyModuleLoader } from 'lazyUtils/lazyModuleImport'
import Loader from 'components/common/loader/Loader'
import IndexSkeleton from 'pages/index/IndexSkeleton'

// Default Imports (user-defined components).
import PrivateRoute from './PrivateRoute'
import PublicRoute from './PublicRoute'
import MainLayout from 'layouts//mainLayout/MainLayout'
import AuthLayout from 'layouts/authLayout/AuthLayout'

const Index = lazyModuleImport(() => import('pages/index/Index'))
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
              <LazyModuleLoader element={<Index />} fallback={<IndexSkeleton />} />
            } />
          </Route>

          {/* Private Routes */}
          <Route element={<PrivateRoute />}>
            <Route path='/home' element={
              <LazyModuleLoader element={<Home />} fallback={<Loader />} />
            } />
          </Route>
        </Route>

        <Route element={<AuthLayout />}>
          <Route path='/signin' element={
            <LazyModuleLoader element={<SigninPage />} fallback={<Loader />} />
          } />
          <Route path='/signup' element={
            <LazyModuleLoader element={<SignupPage />} fallback={<Loader />} />
          } />
        </Route>
        {/* Catch-all route for 404 Not Found */}
        <Route path="*" element={
          <LazyModuleLoader element={<NotFound />} fallback={<Loader />} />
        } />
      </Routes>
    </Router>
  )
}

export default AppRoutes
