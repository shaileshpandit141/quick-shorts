import React, { createContext, ReactNode, useContext, useState } from "react";

interface IsCommentsOpenContextValue {
  isCommentsOpen: boolean;
  toggleIsCommentsOpen: (event: React.MouseEvent<HTMLElement>) => void;
}

const IsCommentsOpenContext = createContext<
  IsCommentsOpenContextValue | undefined
>(undefined);

interface Props {
  children: ReactNode;
}

export const IsCommentsOpenProvider = ({ children }: Props) => {
  const [isCommentsOpen, setIsCommentsOpen] = useState(false);

  const toggleIsCommentsOpen = (event: React.MouseEvent<HTMLElement>) => {
    setIsCommentsOpen((prevState) => !prevState);
  };

  return (
    <IsCommentsOpenContext.Provider
      value={{ isCommentsOpen, toggleIsCommentsOpen }}
    >
      {children}
    </IsCommentsOpenContext.Provider>
  );
};

export const useIsCommentsOpen = () => {
  const context = useContext(IsCommentsOpenContext);
  if (!context) {
    throw new Error(
      "useIsCommentsOpen must be used within a IsCommentsOpenContextProvider",
    );
  }
  return context;
};
