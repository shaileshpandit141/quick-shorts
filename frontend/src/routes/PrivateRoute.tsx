import { Navigate, Outlet } from 'react-router-dom'
import { useSigninSelector } from "features/auth/signin";

const PrivateRoute = (): JSX.Element => {
  const { data } = useSigninSelector()

  if (!(data.refresh_token)) {
    return <Navigate to='/auth/sign-in' replace={true} />
  }

  return <Outlet />
}

export default PrivateRoute
