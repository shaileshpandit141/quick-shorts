import React, { createContext, ReactNode, useContext, useState } from "react";

interface DashboardSmallSidebarContextValue {
  isSidebarOpen: boolean;
  handleOpenSidebar: () => void;
  handleCloseSidebar: () => void;
  handleToggelSidebar: () => void;
}

const DashboardSmaillSidebarContext = createContext<
  DashboardSmallSidebarContextValue | undefined
>(undefined);

interface Props {
  children: ReactNode;
}

export const DashboardSmaillSidebarProvider = ({ children }: Props) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const handleOpenSidebar = () => {
    setIsSidebarOpen(true);
  };

  const handleCloseSidebar = () => {
    setIsSidebarOpen(false);
  };

  const handleToggelSidebar = () => {
    setIsSidebarOpen((prevState) => !prevState);
  };

  return (
    <DashboardSmaillSidebarContext.Provider
      value={{
        isSidebarOpen,
        handleOpenSidebar,
        handleCloseSidebar,
        handleToggelSidebar,
      }}
    >
      {children}
    </DashboardSmaillSidebarContext.Provider>
  );
};

export const useDashboardSmaillSidebar = () => {
  const context = useContext(DashboardSmaillSidebarContext);
  if (!context) {
    throw new Error(
      "useDashboardSmaillSidebar must be used within a DashboardSmaillSidebarProvider",
    );
  }
  return context;
};
