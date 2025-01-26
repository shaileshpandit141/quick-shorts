import React, { useState, useEffect } from 'react';
import Button from 'components/Button/Button';

const InstallAppButton = () => {
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isInstallable, setIsInstallable] = useState(false);
  const [isAppInstalled, setIsAppInstalled] = useState(false);

  useEffect(() => {
    // Check if the app is already installed
    const isStandalone =
      window.matchMedia('(display-mode: standalone)').matches ||
      window.navigator.standalone;

    if (isStandalone) {
      setIsAppInstalled(true);
      return;
    }

    // Listen for the beforeinstallprompt event
    const handleBeforeInstallPrompt = (event) => {
      setDeferredPrompt(event); // Save the event for later
      setIsInstallable(true); // Show the install button
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);

  const handleInstallClick = async () => {
    if (!deferredPrompt) {
      console.warn('Deferred prompt is not available');
      return;
    }

    deferredPrompt.prompt(); // Show the install prompt

    const { outcome } = await deferredPrompt.userChoice; // Wait for user choice
    if (outcome === 'accepted') {
      console.log('User accepted the install prompt');
    } else {
      console.log('User dismissed the install prompt');
    }

    setDeferredPrompt(null); // Reset the deferred prompt
    setIsInstallable(false); // Hide the install button
  };

  // Don't render anything if the app is already installed
  if (isAppInstalled) {
    return null;
  }

  return (
    isInstallable && (
      <Button
        type="icon"
        iconName='installDesktop'
        className='install-app-button'
        onClick={handleInstallClick}
      />
    )
  );
};

export default InstallAppButton;
