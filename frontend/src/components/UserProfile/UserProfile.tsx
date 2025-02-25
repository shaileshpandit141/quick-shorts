import React, { useRef, useEffect } from 'react';
import './UserProfile.css';
import { NavLink, SignoutButton } from 'components'
import { useMenu } from 'hooks';
import { isAuthenticated } from 'utils';
import { user, useUserSelector } from 'features/user';
import { buildMediaURL, getEnv } from 'utils';

const UserProfile: React.FC = (): JSX.Element | null => {

  const button = useRef(null)
  const userProfileRef = useRef(null)
  const { status, data } = useUserSelector()

  const { setVisibleStyle, setHiddenStyle } = useMenu({
    buttonRef: button,
    contentRef: userProfileRef
  })

  useEffect(() => {
    setVisibleStyle((prevStyles) => ({
      ...prevStyles,
      transform: 'scale(1)'
    }))

    setHiddenStyle((prevStyles) => ({
      ...prevStyles,
      transform: 'scale(0.9)'
    }))
  }, [setVisibleStyle, setHiddenStyle])

  useEffect(() => {
    if (status === 'idle' && isAuthenticated()) {
      user()
    }
  }, [status]);

  if (!isAuthenticated() && (status !== 'succeeded')) {
    return null
  }

  return (
    <div className='user-profile'>
      <button
        className='button profile-action-button'
        ref={button}
      >
        {data?.avatar && (
          <img src={buildMediaURL(data?.avatar)} alt='avatar-image' />
        )}
      </button>
      <div
        className='user-profile-card-container'
        ref={userProfileRef}
      >
        <div className='user-profile-header-card'>
          <section className='user-profile-image'>
            {data?.avatar && (
              <img src={buildMediaURL(data?.avatar)} alt='avatar-image' />
            )}
          </section>
          <section className='user-profile-info'>
            <h6 className='username'>{data?.username}</h6>
            <p className='email'>{data?.email}</p>
          </section>
          <NavLink
            to={`${getEnv("BASE_API_URL")}/admin/`}
            type='link'
            className='edit-profile'
            target='_blank'
          >Django Admin</NavLink>
          <SignoutButton />
        </div>
      </div>
    </div>
  )
}

export default UserProfile;
