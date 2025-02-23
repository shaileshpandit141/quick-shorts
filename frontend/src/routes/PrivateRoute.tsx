import { Navigate, Outlet } from 'react-router-dom'
import { useSigninUserSelector } from "features/auth/signin";

const PrivateRoute = (): JSX.Element => {
  const { data } = useSigninUserSelector()

  if (!(data.refresh_token)) {
    return <Navigate to='/auth/sign-in' replace={true} />
  }

  return <Outlet />
}

export default PrivateRoute
