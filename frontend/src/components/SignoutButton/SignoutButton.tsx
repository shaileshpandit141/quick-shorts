import React, { useEffect } from 'react';
import './SignoutButton.css';
import { Navigate } from 'react-router-dom';
import Button from 'components/Button/Button';
import { isAuthenticated } from 'utils/isAuthenticted';
import { resetSigninState } from 'features/auth';
import { useDispatch } from 'react-redux';
import { signoutThunk } from 'features/auth';
import { useSignoutSelector } from 'features/auth';
import { useSigninSelector } from 'features/auth';

const SignoutButton: React.FC = () => {
  const dispatch = useDispatch();
  const { status } = useSignoutSelector();
  const signinState = useSigninSelector();

  const handleSignout = (event: React.MouseEvent<HTMLButtonElement>) => {
    dispatch(signoutThunk({
      refresh_token: signinState.data?.refresh_token || ''
    }) as any);
  };

  useEffect(() => {
    if (status === 'succeeded') {
      dispatch(resetSigninState());
    }
  }, [status, dispatch]);

  if (!isAuthenticated()) {
    return null
  }

  if (status === 'succeeded') {
    return <Navigate to='/sign-in' />
  }

  return (
    <Button
      type='button'
      iconName='signout'
      label='sign out'
      className='signout-button'
      onClick={handleSignout}
      isLoaderOn={status === 'loading'}
    />
  )
}

export default SignoutButton;
