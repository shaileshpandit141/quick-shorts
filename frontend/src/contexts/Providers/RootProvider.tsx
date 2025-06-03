import { ReactNode } from "react";
import { SidebarProvider } from "../features/SidebarProvider";
import { VideoProvider } from "contexts/features/VideoContext";
import { IsCommentsOpenProvider } from "contexts/features/IsCommentsOpen";

interface Props {
  children: ReactNode;
}

const RootProvider = ({ children }: Props) => {
  return (
    <SidebarProvider>
      <VideoProvider>
        <IsCommentsOpenProvider>{children}</IsCommentsOpenProvider>
      </VideoProvider>
    </SidebarProvider>
  );
};

export default RootProvider;
