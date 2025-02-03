import React from 'react';
import "./AppLogoImage.css"
import AppLogo from 'assets/images/appLogo.png';

interface AppLogoImageProps {
  size?: number
}

const AppLogoImage: React.FC<AppLogoImageProps> = (props) => {

  const size = props.size ? props.size : 40

  const styles = {
    height: `${size}px`,
    width: `${size}px`
  }

  return (
    <figure
      className='app-logo-image'
      style={styles}
    >
      <img
        src={AppLogo}
        alt='logo-image'
        style={styles}
      />
    </figure>
  )
}

export default AppLogoImage;
