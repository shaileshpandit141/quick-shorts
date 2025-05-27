import React, { ReactNode } from "react";
import { SidebarProvider } from "../features/SidebarProvider";
import { DashboardSmaillSidebarProvider } from "../features/DashboardSmaillSidebarProvider";
import { MuteContextProvider } from "contexts/features/MuteContext"
interface Props {
  children: ReactNode;
}

const RootProvider = ({ children }: Props) => {
  return (
    <SidebarProvider>
      <DashboardSmaillSidebarProvider>
        <MuteContextProvider>
          {children}
        </MuteContextProvider>
      </DashboardSmaillSidebarProvider>
    </SidebarProvider>
  );
};

export default RootProvider;
