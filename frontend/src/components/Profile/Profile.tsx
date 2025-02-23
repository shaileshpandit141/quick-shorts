import React, { useRef, useEffect } from 'react';
import './Profile.css';
import { NavLink, SignoutButton } from 'components'
import { useMenu } from 'hooks';
import { isAuthenticated } from 'utils';
import { user, useUserSelector } from 'features/user';
import { get_absolute_url } from 'utils';

const Profile: React.FC = (): JSX.Element | null => {

  const button = useRef(null)
  const profile = useRef(null)
  const { status, data } = useUserSelector()

  const { setVisibleStyle, setHiddenStyle } = useMenu({
    buttonRef: button,
    contentRef: profile
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
    <div className='profile'>
      <button
        className='button profile-action-button'
        ref={button}
      >
        {data?.avatar && (
          <img src={get_absolute_url(data?.avatar)} alt='avatar-image' />
        )}
      </button>
      <div
        className='profile-card-container'
        ref={profile}
      >
        <div className='profile-header-card'>
          <section className='profile-image'>
            {data?.avatar && (
              <img src={get_absolute_url(data?.avatar)} alt='avatar-image' />
            )}
          </section>
          <section className='profile-info'>
            <h6 className='username'>{data?.username}</h6>
            <p className='email'>{data?.email}</p>
          </section>
          <NavLink
            to={get_absolute_url('/admin/')}
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

export default Profile;
