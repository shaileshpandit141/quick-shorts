import React, { createContext, ReactNode, useContext, useState } from "react";

interface VideoContextValue {
  isMuted: boolean;
  toggleMute: () => void;
}

const VideoContext = createContext<VideoContextValue | undefined>(undefined);

interface Props {
  children: ReactNode;
}

export const VideoProvider = ({ children }: Props) => {
  const [isMuted, setIsMuted] = useState<boolean>(true);

  const toggleMute = () => {
    setIsMuted((prev) => !prev);
  };

  return (
    <VideoContext.Provider value={{ isMuted, toggleMute }}>
      {children}
    </VideoContext.Provider>
  );
};

export const useVideo = () => {
  const context = useContext(VideoContext);
  if (!context) {
    throw new Error("useVideo must be used within a VideoContextProvider");
  }
  return context;
};
