import React from 'react'
import { Outlet } from 'react-router-dom'

const PublicRoute = (): JSX.Element => {
  return (
    <Outlet />
  )
}

export default PublicRoute
