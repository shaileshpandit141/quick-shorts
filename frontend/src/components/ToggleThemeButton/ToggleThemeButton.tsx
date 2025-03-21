import React, { useState, useEffect } from "react";
import "./ToggleThemeButton.css";
import { Button } from "components";

type Theme = "light" | "dark";

const ToggleThemeButton: React.FC = () => {
  // Check localStorage first, then system preference
  const getInitialTheme = (): Theme => {
    const savedTheme = localStorage.getItem("theme") as Theme;
    return (
      savedTheme ||
      (window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light")
    );
  };

  const [theme, setTheme] = useState<Theme>(getInitialTheme);

  // Apply theme when it changes
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  // Handle system theme changes dynamically
  useEffect(() => {
    const mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");

    const handleSystemThemeChange = (event: MediaQueryListEvent) => {
      if (localStorage.getItem("theme")) {
        setTheme(event.matches ? "dark" : "light");
      }
    };

    mediaQuery.addEventListener("change", handleSystemThemeChange);
    return () =>
      mediaQuery.removeEventListener("change", handleSystemThemeChange);
  }, []);

  // Toggle theme manually
  const handleToggleTheme = () =>
    setTheme((prev) => (prev === "light" ? "dark" : "light"));

  return (
    <Button
      type="icon"
      icon={theme === "light" ? "lightModeIcon" : "darkModeIcon"}
      onClick={handleToggleTheme}
      className="toggle-theme-button"
    />
  );
};

export default ToggleThemeButton;
