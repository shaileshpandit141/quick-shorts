import React, { useEffect } from 'react';
import './SignoutButton.css';
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
import { dispatchResetUserState } from 'features/user';

const SignoutButton: React.FC = () => {
  const { status } = useSignoutSelector();
  const signinState = useSigninSelector();

  const handleSignout = (event: React.MouseEvent<HTMLButtonElement>) => {
    dispatchSignoutAction({
      refresh_token: signinState.data?.refresh_token || ''
    })
  };

  useEffect(() => {
    if (status !== 'idle') {
      dispatchResetSigninState();
      dispatchResetUserState();
      triggerToast("success", "You have been successfully signed out")
    }
  }, [status]);

  if (!isAuthenticated()) {
    return null
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
