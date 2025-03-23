import React, { useState, useEffect, JSX } from "react";
import Button from "components/Common/Button/Button";

interface BeforeInstallPromptEvent extends Event {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: "accepted" | "dismissed"; platform: string }>;
}

const InstallAppButton: React.FC = (): JSX.Element | null => {
  const [deferredPrompt, setDeferredPrompt] =
    useState<BeforeInstallPromptEvent | null>(null);
  const [isInstallable, setIsInstallable] = useState<boolean>(false);
  const [isAppInstalled, setIsAppInstalled] = useState<boolean>(false);

  useEffect(() => {
    // Check if the app is already installed
    const isStandalone =
      window.matchMedia("(display-mode: standalone)").matches ||
      // Some browsers have window.navigator.standalone
      // @ts-ignore
      window.navigator.standalone;

    if (isStandalone) {
      setIsAppInstalled(true);
      return;
    }

    const handleBeforeInstallPrompt = (event: Event) => {
      event.preventDefault(); // Prevent the default mini-infobar
      setDeferredPrompt(event as BeforeInstallPromptEvent);
      setIsInstallable(true);
    };

    window.addEventListener("beforeinstallprompt", handleBeforeInstallPrompt);

    return () => {
      window.removeEventListener(
        "beforeinstallprompt",
        handleBeforeInstallPrompt,
      );
    };
  }, []);

  const handleInstallClick = async (): Promise<void> => {
    if (!deferredPrompt) {
      console.warn("Deferred prompt is not available");
      return;
    }

    await deferredPrompt.prompt();
    const { outcome } = await deferredPrompt.userChoice;
    if (outcome === "accepted") {
      console.log("User accepted the install prompt");
    } else {
      console.log("User dismissed the install prompt");
    }
    setDeferredPrompt(null);
    setIsInstallable(false);
  };

  if (isAppInstalled) {
    return null;
  }

  return isInstallable ? (
    <Button
      type="icon"
      icon="installDesktop"
      className="install-app-button"
      onClick={handleInstallClick}
    />
  ) : null;
};

export default InstallAppButton;
