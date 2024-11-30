// Named Imports (external libraries).
import React from 'react'
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom'
import { lazyModuleImport, LazyModuleLoader } from 'lazyUtils/lazyModuleImport'
import Loader from 'componsnts/common/loader/Loader'
import IndexSkeleton from 'pages/index/IndexSkeleton'

// Default Imports (user-defined components).
import PrivateRoute from './PrivateRoute'
import PublicRoute from './PublicRoute'
import MainLayout from 'layouts//mainLayout/MainLayout'
import AuthLayout from 'layouts/authLayout/AuthLayout'

const Index = lazyModuleImport(() => import('pages/index/Index'))
const Home = lazyModuleImport(() => import('pages/home/Home'))
const Signin = lazyModuleImport(() => import('pages/signin/Signin'))
const Signup = lazyModuleImport(() => import('pages/signup/Signup'))
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
            <LazyModuleLoader element={<Signin />} fallback={<Loader />} />
          } />
          <Route path='/signup' element={
            <LazyModuleLoader element={<Signup />} fallback={<Loader />} />
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
