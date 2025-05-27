import React, { ReactNode } from "react";
import { SidebarProvider } from "../features/SidebarProvider";
import { MuteContextProvider } from "contexts/features/MuteContext"
interface Props {
  children: ReactNode;
}

const RootProvider = ({ children }: Props) => {
  return (
    <SidebarProvider>
      <MuteContextProvider>
        {children}
      </MuteContextProvider>
    </SidebarProvider>
  );
};

export default RootProvider;
