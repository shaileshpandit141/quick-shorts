import React from 'react'
import './AppLogo.css'

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
      <img
        src='logo512.png'
        alt='logo-image'
        style={styles}
      />
    </figure>
  )
}

export default AppLogo
