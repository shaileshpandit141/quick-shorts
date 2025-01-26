import React, { useRef, useEffect } from 'react';
import './Profile.css';
import { } from 'components';
import { useMenu } from 'hooks';

const Profile: React.FC = (): JSX.Element => {

  const button = useRef(null)
  const profile = useRef(null)

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

  return (
    <div className='profile'>
      <button
        className='button profile-action-button'
        ref={button}
      >
        <img src='logo192.png' alt='logo192.png' />
      </button>
      <div
        className='profile-card-container'
        ref={profile}
      >
        <div className='profile-header-card'>
          <section className='profile-image'>
            <img src='logo192.png' alt='logo192.png' />
          </section>
          <section className='profile-info'>
            <h6 className='username'>username</h6>
            <p className='email'>username@gmail.com</p>
          </section>
        </div>
      </div>
    </div>
  )
}

export default Profile;
