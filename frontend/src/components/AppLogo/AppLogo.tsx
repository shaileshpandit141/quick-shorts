import React from 'react'
import './AppLogo.css'
import AppLogoImage from './AppLogoImage';

interface LogoProps {
  size?: number
}

const AppLogo: React.FC<LogoProps> = (props) => {

  const size = props.size ? props.size : 40

  const styles = {
    height: `${size}px`,
    width: `${size}px`
  }

  return (
    <figure
      className='logo-container'
      style={styles}
    >
      <AppLogoImage styles={styles} />
    </figure>
  )
}

export default AppLogo
