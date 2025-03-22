import React, { createContext, ReactNode, useContext, useState } from "react";

interface MainSidebarContextValue {
  isSidebarOpen: boolean;
  handleOpenSidebar: () => void;
  handleCloseSidebar: () => void;
  handleToggelSidebar: () => void;
}

const MainSidebarContext = createContext<MainSidebarContextValue | undefined>(
  undefined,
);

interface Props {
  children: ReactNode;
}

export const MainSidebarProvider = ({ children }: Props) => {
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
    <MainSidebarContext.Provider
      value={{
        isSidebarOpen,
        handleOpenSidebar,
        handleCloseSidebar,
        handleToggelSidebar,
      }}
    >
      {children}
    </MainSidebarContext.Provider>
  );
};

export const useMainSidebar = () => {
  const context = useContext(MainSidebarContext);
  if (!context) {
    throw new Error("useSidebar must be used within a MainSidebarProvider");
  }
  return context;
};
