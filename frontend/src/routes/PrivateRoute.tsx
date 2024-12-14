import { Navigate, Outlet } from 'react-router-dom'
import authActions from "features/auth";

const PrivateRoute = (): JSX.Element => {
  const { data } = authActions.useSigninSelector()

  if (!(data.refresh_token)) {
    return <Navigate to='/signin' replace={true} />
  }

  return <Outlet />
}

export default PrivateRoute
