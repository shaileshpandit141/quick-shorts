import React, { lazy, ReactElement, Suspense } from 'react'
import { SvgIconProps } from '@mui/material'
import { LazyIconMapType } from './LazyIcon.types'

const iconsMap: LazyIconMapType = {
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
  reTry: lazy(() => import('@mui/icons-material/ReplayRounded')),
  search: lazy(() => import('@mui/icons-material/SearchRounded')),
  installDesktop: lazy(() => import('@mui/icons-material/InstallDesktopRounded')),
  close: lazy(() => import('@mui/icons-material/CloseRounded')),
  success: lazy(() => import('@mui/icons-material/DoneAllRounded')),
  info: lazy(() => import('@mui/icons-material/InfoRounded')),
  error: lazy(() => import('@mui/icons-material/ErrorRounded')),
  warning: lazy(() => import('@mui/icons-material/WarningAmberRounded')),
  menuOpen: lazy(() => import('@mui/icons-material/MenuOpenRounded')),
  checkCircle: lazy(() => import('@mui/icons-material/CheckCircleRounded')),
  click: lazy(() => import('@mui/icons-material/AdsClickRounded')),
}

interface LazyIconProps extends SvgIconProps {
  iconName: keyof LazyIconMapType
  fallback?: ReactElement
}

const LazyIcon = ({ iconName, fallback, ...props }: LazyIconProps) => {
  const IconComponent = iconsMap[iconName]

  return (
    <Suspense fallback={fallback}>
      <IconComponent {...props} />
    </Suspense>
  )
}

export { LazyIcon }
