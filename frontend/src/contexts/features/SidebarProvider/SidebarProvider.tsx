import React, { createContext, ReactNode, useContext, useState } from "react";

interface SidebarContextValue {
  isSidebarOpen: boolean;
  handleOpenSidebar: () => void;
  handleCloseSidebar: () => void;
  handleToggelSidebar: () => void;
}

const SidebarContext = createContext<SidebarContextValue | undefined>(
  undefined,
);

interface Props {
  children: ReactNode;
}

export const SidebarProvider = ({ children }: Props) => {
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
    <SidebarContext.Provider
      value={{
        isSidebarOpen,
        handleOpenSidebar,
        handleCloseSidebar,
        handleToggelSidebar,
      }}
    >
      {children}
    </SidebarContext.Provider>
  );
};

export const useSidebar = () => {
  const context = useContext(SidebarContext);
  if (!context) {
    throw new Error("useSidebar must be used within a SidebarProvider");
  }
  return context;
};
