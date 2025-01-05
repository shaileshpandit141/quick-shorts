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
import { triggerToast } from 'utils/toast';

const SignoutButton: React.FC = () => {
  const dispatch = useDispatch();
  const { status, message } = useSignoutSelector();
  const signinState = useSigninSelector();

  const handleSignout = (event: React.MouseEvent<HTMLButtonElement>) => {
    dispatch(signoutThunk({
      refresh_token: signinState.data?.refresh_token || ''
    }) as any);
  };

  useEffect(() => {
    if (status === 'succeeded') {
      dispatch(resetSigninState());
      triggerToast(dispatch, "success", message)
    } else if (status === 'failed') {
      triggerToast(dispatch, "error", message)
    }
  }, [status, dispatch, message]);

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
