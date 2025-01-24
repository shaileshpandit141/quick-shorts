import React, { useState, useEffect, useCallback } from 'react';
import './Drawer.css';

interface DrawerProps {
  children: React.ReactNode;
  isOpen: boolean;
  onClick?: (event: React.MouseEvent<HTMLElement>) => void;
  className?: string;
  style?: React.CSSProperties;
}

const TRANSITION_DURATION = 300;

const Drawer: React.FC<DrawerProps> = (
  { children, onClick, isOpen, className, style }
): JSX.Element | null => {
  const [isDeactivated, setIsDeactivated] = useState(false);
  const [isTransitioning, setIsTransitioning] = useState(false);

  const handleTransition = useCallback((
    shouldDeactivate: boolean
  ) => {
    setIsTransitioning(true);
    if (shouldDeactivate) {
      setIsDeactivated(false);
    }

    const timer = setTimeout(() => {
      setIsTransitioning(false);
      if (!shouldDeactivate) {
        setIsDeactivated(true);
      }
    }, TRANSITION_DURATION);

    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    return isOpen ? handleTransition(true) : handleTransition(false);
  }, [isOpen, handleTransition]);

  const handleClick = useCallback((event: React.MouseEvent<HTMLElement>) => {
    event.stopPropagation();
    if (onClick && !isTransitioning) {
      onClick(event);
    }
  }, [onClick, isTransitioning]);

  if (isDeactivated && !isOpen) {
    return null;
  }

  const drawerClassName = `drawer ${className || ''} ${isOpen ? 'drawer--active' : 'drawer--inactive'}`;

  return (
    <div
      className={drawerClassName}
      onClick={handleClick}
      style={style}
    >
      {children}
    </div>
  );
};

export default Drawer;
