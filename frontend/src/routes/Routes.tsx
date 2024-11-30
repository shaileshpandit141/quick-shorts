// Named Imports (external libraries).
import React from 'react'
import {
  BrowserRouter as Router,
  Routes,
  Route
} from 'react-router-dom'

// Default Imports (user-defined components).
import PrivateRoute from './PrivateRoute'
import PublicRoute from './PublicRoute'
import MainLayout from 'layouts//mainLayout/MainLayout'
import AuthLayout from 'layouts/authLayout/AuthLayout'
import Index from 'pages/index/Index'
import Home from 'pages/home/Home'
import Signin from 'pages/signin/Signin'
import Signup from 'pages/signup/Signup'
import NotFound from 'pages/NotFound/NotFound'

const AppRoutes: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route element={<MainLayout />}>

          {/* Public Routes */}
          <Route element={<PublicRoute />}>
            <Route index element={<Index />} />
          </Route>

          {/* Private Routes */}
          <Route element={<PrivateRoute />}>
            <Route path='/home' element={<Home />} />
          </Route>
        </Route>

        <Route element={<AuthLayout />}>
          <Route path='/signin' element={<Signin />} />
          <Route path='/signup' element={<Signup />} />
        </Route>
        {/* Catch-all route for 404 Not Found */}
        <Route path="*" element={<NotFound />} />
      </Routes>
    </Router>
  )
}

export default AppRoutes
