import React, { ReactNode } from "react";
import { SidebarProvider } from "../features/SidebarProvider";
import { DashboardSmaillSidebarProvider } from "../features/DashboardSmaillSidebarProvider";

interface Props {
  children: ReactNode;
}

const RootProvider = ({ children }: Props) => {
  return (
    <SidebarProvider>
      <DashboardSmaillSidebarProvider>
        {children}
      </DashboardSmaillSidebarProvider>
    </SidebarProvider>
  );
};

export default RootProvider;
