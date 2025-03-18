import React, { ReactNode } from "react";
import { SidebarProvider } from "../features/SidebarProvider";


interface Props {
  children: ReactNode;
}

const RootProvider = ({ children }: Props) => {

  return (
    <SidebarProvider>
      {children}
    </SidebarProvider>
  );
};

export default RootProvider;
