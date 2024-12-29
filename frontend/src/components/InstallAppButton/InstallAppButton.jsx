import React, { useState, useEffect, useCallback, memo } from 'react';
import './InstallAppButton.css';
import { LazyIconImport } from 'lazyUtils/LazyIconImport/LazyIconImport';

const InstallAppButton = memo(() => {
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isInstallable, setIsInstallable] = useState(false);
  const [isAppInstalled, setIsAppInstalled] = useState(false);

  useEffect(() => {
    // Check if the app is already installed
    const isStandalone = window.matchMedia('(display-mode: standalone)').matches ||
      window.navigator.standalone;

    if (isStandalone) {
      setIsAppInstalled(true);
      return;
    }

    // Listen for the beforeinstallprompt event
    const handleBeforeInstallPrompt = (event) => {
      event.preventDefault();
      setDeferredPrompt(event);
      setIsInstallable(true);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);

  const handleInstallClick = useCallback(() => {
    if (!deferredPrompt) return;

    // Show the install prompt
    deferredPrompt.prompt();

    deferredPrompt.userChoice
      .then((choiceResult) => {
        if (choiceResult.outcome === 'accepted') {
          console.log('User accepted the install prompt');
        } else {
          console.log('User dismissed the install prompt');
        }
        setDeferredPrompt(null);
        setIsInstallable(false);
      })
      .catch((err) => {
        console.error('Error during install prompt:', err);
      });
  }, [deferredPrompt]);

  if (isAppInstalled) {
    return null;
  }

  return (
    isInstallable && (
      <button
        className='button install-app-button'
        onClick={handleInstallClick}
      >
        <span className='icon'>
          <LazyIconImport icon="InstallDesktop" />
        </span>
        <span className='label'>
          Install
        </span>
      </button>
    )
  );
});

export default InstallAppButton;
