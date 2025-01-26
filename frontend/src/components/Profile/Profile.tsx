import React, { useRef, useEffect } from 'react';
import './Profile.css';
import { useDispatch } from 'react-redux';
import { AnchorLink } from 'components'
import { useMenu } from 'hooks';
import { isAuthenticated } from 'features/auth';
import { dispatchUserAction, useUserSelector } from 'features/user';
import { get_absolute_url } from 'utils';

const Profile: React.FC = (): JSX.Element | null => {

  const button = useRef(null)
  const profile = useRef(null)
  const dispatch = useDispatch()
  const { data } = useUserSelector()

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
    dispatchUserAction(dispatch)
  }, [dispatch]);

  if (!isAuthenticated()) {
    return null
  }

  return (
    <div className='profile'>
      <button
        className='button profile-action-button'
        ref={button}
      >
        <img src={get_absolute_url(data?.avatar)} alt='avatar-image' />
      </button>
      <div
        className='profile-card-container'
        ref={profile}
      >
        <div className='profile-header-card'>
          <section className='profile-image'>
            <img src={get_absolute_url(data?.avatar)} alt='avatar-image' />
          </section>
          <section className='profile-info'>
            <h6 className='username'>{data?.username}</h6>
            <p className='email'>{data?.email}</p>
          </section>
          <AnchorLink
            to={get_absolute_url('/admin/')}
            type='link'
          >Admin</AnchorLink>
        </div>
      </div>
    </div>
  )
}

export default Profile;
