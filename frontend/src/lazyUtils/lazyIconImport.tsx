import React, { lazy, ReactElement, Suspense } from 'react'
import { SvgIconProps } from '@mui/material'

interface IconsMapType {
  signin: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  signout: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  signup: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  settings: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  person: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  accountCircle: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  arrowBack: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  arrowUp: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  lightModeIcon: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  darkModeIcon: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  eyeClose: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  eyeOpen: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  circleAppIcon: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  reTry: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
  search: React.LazyExoticComponent<React.ComponentType<SvgIconProps>>
}

const iconsMap: IconsMapType = {
  signin: lazy(() => import('@mui/icons-material/LoginRounded')),
  signout: lazy(() => import('@mui/icons-material/LogoutRounded')),
  signup: lazy(() => import('@mui/icons-material/AppRegistrationRounded')),
  settings: lazy(() => import('@mui/icons-material/Settings')),
  person: lazy(() => import('@mui/icons-material/PersonRounded')),
  accountCircle: lazy(() => import('@mui/icons-material/AccountCircleRounded')),
  arrowBack: lazy(() => import('@mui/icons-material/ArrowBackIosNewRounded')),
  arrowUp: lazy(() => import('@mui/icons-material/ArrowUpwardRounded')),
  lightModeIcon: lazy(() => import('@mui/icons-material/WbSunnyRounded')),
  darkModeIcon: lazy(() => import('@mui/icons-material/DarkModeRounded')),
  eyeClose: lazy(() => import('@mui/icons-material/RemoveRedEyeRounded')),
  eyeOpen: lazy(() => import('@mui/icons-material/RemoveRedEyeOutlined')),
  circleAppIcon: lazy(() => import('@mui/icons-material/Brightness1Rounded')),
  reTry: lazy(() => import('@mui/icons-material/ReplayRounded')),
  search: lazy(() => import('@mui/icons-material/SearchRounded')),
}

interface LazyIconImportProps extends SvgIconProps {
  icon: keyof IconsMapType
  fallback?: ReactElement
}

const LazyIconImport = ({ icon, fallback = <span />, ...props }: LazyIconImportProps) => {
  const IconComponent = iconsMap[icon]

  return (
    <Suspense fallback={fallback}>
      <IconComponent {...props} />
    </Suspense>
  )
}

export { LazyIconImport }
