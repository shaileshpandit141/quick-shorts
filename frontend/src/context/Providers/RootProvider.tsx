import React, { ReactNode } from "react";
import { MainSidebarProvider } from "../features/MainSidebarProvider";
import { DashboardSmaillSidebarProvider } from "../features/DashboardSmaillSidebarProvider";

interface Props {
  children: ReactNode;
}

const RootProvider = ({ children }: Props) => {
  return (
    <MainSidebarProvider>
      <DashboardSmaillSidebarProvider>
        {children}
      </DashboardSmaillSidebarProvider>
    </MainSidebarProvider>
  );
};

export default RootProvider;
