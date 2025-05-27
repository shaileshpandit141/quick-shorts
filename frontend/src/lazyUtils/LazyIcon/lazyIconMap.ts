import { lazy } from "react";

export const lazyIconMap = {
  signin: lazy(() => import("@mui/icons-material/LoginRounded")),
  signout: lazy(() => import("@mui/icons-material/LogoutRounded")),
  signup: lazy(() => import("@mui/icons-material/AppRegistrationRounded")),
  settings: lazy(() => import("@mui/icons-material/Settings")),
  person: lazy(() => import("@mui/icons-material/PersonRounded")),
  accountCircle: lazy(() => import("@mui/icons-material/AccountCircleRounded")),
  arrowBack: lazy(() => import("@mui/icons-material/ArrowBackIosNewRounded")),
  arrowUp: lazy(() => import("@mui/icons-material/ArrowUpwardRounded")),
  lightModeIcon: lazy(() => import("@mui/icons-material/WbSunnyRounded")),
  darkModeIcon: lazy(() => import("@mui/icons-material/DarkModeRounded")),
  eyeClose: lazy(() => import("@mui/icons-material/RemoveRedEyeRounded")),
  eyeOpen: lazy(() => import("@mui/icons-material/RemoveRedEyeOutlined")),
  reTry: lazy(() => import("@mui/icons-material/ReplayRounded")),
  search: lazy(() => import("@mui/icons-material/SearchRounded")),
  installDesktop: lazy(
    () => import("@mui/icons-material/InstallDesktopRounded")
  ),
  close: lazy(() => import("@mui/icons-material/CloseRounded")),
  success: lazy(() => import("@mui/icons-material/DoneAllRounded")),
  info: lazy(() => import("@mui/icons-material/InfoRounded")),
  error: lazy(() => import("@mui/icons-material/ErrorRounded")),
  warning: lazy(() => import("@mui/icons-material/WarningAmberRounded")),
  sidebarIcon: lazy(() => import("@mui/icons-material/SortRounded")),
  checkCircle: lazy(() => import("@mui/icons-material/CheckCircleRounded")),
  click: lazy(() => import("@mui/icons-material/AdsClickRounded")),
  supervisorAccountIcon: lazy(
    () => import("@mui/icons-material/SupervisorAccount")
  ),
  dashboardIcon: lazy(() => import("@mui/icons-material/DashboardRounded")),
  volumeOff: lazy(() => import("@mui/icons-material/VolumeOffRounded")),
  volumeOn: lazy(() => import("@mui/icons-material/VolumeUpRounded")),
};
