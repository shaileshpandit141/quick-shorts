import React, { createContext, ReactNode, useContext, useState } from "react";

interface MuteContextValue {
  isMuted: boolean;
  toggleMute: () => void;
}

const MuteContext = createContext<MuteContextValue | undefined>(
  undefined,
);

interface Props {
  children: ReactNode;
}

export const MuteContextProvider = ({ children }: Props) => {
  const [isMuted, setIsMuted] = useState<boolean>(true);

  const toggleMute = () => {
    setIsMuted(prev => !prev);
  };

  return (
    <MuteContext.Provider
      value={{ isMuted, toggleMute }}
    >
      {children}
    </MuteContext.Provider>
  );
};

export const useMuteContext = () => {
  const context = useContext(MuteContext);
  if (!context) {
    throw new Error("useMuteContext must be used within a MuteContextProvider");
  }
  return context;
};
