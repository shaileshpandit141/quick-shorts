import React from 'react'
import './AppLogo.css'
import { lazyModuleImport, LazyModuleLoader } from 'lazyUtils/lazyModuleImport'
import { CircularProgress } from '@mui/material';

const AppLogoImage = lazyModuleImport(() => import('./AppLogoImage'))

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
      <LazyModuleLoader
        element={
          <AppLogoImage styles={styles} />
        }
        fallback={
          <CircularProgress />
        }
      />
    </figure>
  )
}

export default AppLogo
