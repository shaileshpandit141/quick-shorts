import React, { useEffect } from 'react';
import './SignoutButton.css';
import { Navigate } from 'react-router-dom';
import Button from 'components/Button/Button';
import {
  dispatchResetSigninState,
  useSigninSelector
} from 'features/auth/signin';
import {
  dispatchSignoutAction,
  useSignoutSelector
} from 'features/auth/signout';
import { isAuthenticated } from 'utils';
import { triggerToast } from 'features/toast';

const SignoutButton: React.FC = () => {
  const { status, message } = useSignoutSelector();
  const signinState = useSigninSelector();

  const handleSignout = (event: React.MouseEvent<HTMLButtonElement>) => {
    dispatchSignoutAction({
      refresh_token: signinState.data?.refresh_token || ''
    })
  };

  useEffect(() => {
    if (status === 'succeeded') {
      dispatchResetSigninState();
      triggerToast("success", message)
    } else if (status === 'failed') {
      triggerToast("error", message)
    }
  }, [status, message]);

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
      className='signout-button'
      onClick={handleSignout}
      isLoaderOn={status === 'loading'}
    >sign in</Button>
  )
}

export default SignoutButton;
