import { ReactElement, Suspense } from "react";
import { SvgIconProps } from "@mui/material";
import { lazyIconMap } from "./lazyIconMap";
import { LazyIconMapType } from "./LazyIconMap.types";

interface RenderLazyIconProps extends SvgIconProps {
  icon: LazyIconMapType;
  fallback?: ReactElement;
}

const RenderLazyIcon = ({ icon, fallback, ...props }: RenderLazyIconProps) => {
  const IconComponent = lazyIconMap[icon];

  return (
    <Suspense fallback={fallback}>
      <IconComponent {...props} />
    </Suspense>
  );
};

export { RenderLazyIcon };
