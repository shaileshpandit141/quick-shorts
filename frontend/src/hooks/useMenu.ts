import { useState, useEffect, useCallback } from "react";
import { RefObject } from "react";
import { useLocation } from "react-router-dom";

interface MenuStyle {
  opacity?: number;
  pointerEvents?: "none" | "auto";
  [key: string]: string | number | undefined;
}

type MenuRefs = {
  buttonRef: RefObject<HTMLElement>;
  contentRef: RefObject<HTMLElement>;
};

const DEFAULT_VISIBLE_STYLE: MenuStyle = {
  opacity: 1,
  pointerEvents: "auto",
};

const DEFAULT_HIDDEN_STYLE: MenuStyle = {
  opacity: 0,
  pointerEvents: "none",
};

export function useMenu({ buttonRef, contentRef }: MenuRefs) {
  const [isVisible, setIsVisible] = useState(false);
  const [visibleStyle, setVisibleStyle] = useState<MenuStyle>(
    DEFAULT_VISIBLE_STYLE,
  );
  const location = useLocation();
  const [hiddenStyle, setHiddenStyle] =
    useState<MenuStyle>(DEFAULT_HIDDEN_STYLE);

  // Handler to toggle menu state
  const toggleMenu = useCallback(() => {
    setIsVisible((prev) => !prev);
  }, []);

  // Handler to handle menu close
  const closeMenu = useCallback(() => {
    setIsVisible(false);
  }, []);

  const getButtonClassName = useCallback(() => {
    if (!buttonRef.current) return "";
    const classes = Array.from(buttonRef.current.classList);
    if (!classes.length) {
      throw new Error("Menu button must have at least one class name");
    }
    return classes[0];
  }, [buttonRef]);

  const handleClickOutside = useCallback(
    (event: MouseEvent) => {
      if (
        contentRef.current &&
        !contentRef.current.contains(event.target as Node) &&
        !(event.target as Element).closest(`.${getButtonClassName()}`)
      ) {
        setIsVisible(false);
      }
    },
    [contentRef, getButtonClassName],
  );

  useEffect(() => {
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [handleClickOutside]);

  useEffect(() => {
    const buttonElement = buttonRef.current;
    if (buttonElement) {
      buttonElement.addEventListener("click", toggleMenu);
      return () => buttonElement.removeEventListener("click", toggleMenu);
    }
  }, [toggleMenu, buttonRef]);

  useEffect(() => {
    if (contentRef.current) {
      const currentStyle = isVisible ? visibleStyle : hiddenStyle;
      Object.assign(contentRef.current.style, {
        position: "absolute",
        zIndex: "999",
        ...currentStyle,
      });
    }
  }, [hiddenStyle, visibleStyle, isVisible, contentRef]);

  // Close menu when navigating to another route
  useEffect(() => {
    closeMenu();
  }, [location, closeMenu]);

  return { toggleMenu, setVisibleStyle, setHiddenStyle };
}
