import React from 'react'
import AppLogo from 'assets/images/appLogo.png'

interface AppLogoImageProps {
  styles: {
    height: string
    width: string
  }
}

const AppLogoImage: React.FC<AppLogoImageProps> = (props) => {

  const { styles } = props
  return (
    <img
      src={AppLogo}
      alt='logo-image'
      style={styles}
    />
  )
}

export default AppLogoImage
