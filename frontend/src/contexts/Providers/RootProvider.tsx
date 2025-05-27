import React, { ReactNode } from "react";
import { SidebarProvider } from "../features/SidebarProvider";
import { VideoProvider } from "contexts/features/VideoContext";
interface Props {
  children: ReactNode;
}

const RootProvider = ({ children }: Props) => {
  return (
    <SidebarProvider>
      <VideoProvider>{children}</VideoProvider>
    </SidebarProvider>
  );
};

export default RootProvider;
