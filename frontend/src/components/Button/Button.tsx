import React from "react";
import "./Button.css";
import { LazyIconMapType, RenderLazyIcon } from "lazyUtils";
import Loader from "components/Loader/Loader";

interface ButtonProps {
  type: "button" | "submit" | "reset" | "icon";
  icon?: LazyIconMapType;
  children?: string | React.ReactNode;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  className?: string;
  isDisabled?: boolean;
  isLoaderOn?: boolean;
  testID?: string;
  accessibilityLabel?: string;
  title?: string;
  ref?: React.RefObject<HTMLButtonElement>;
}

const Button: React.FC<ButtonProps> = (props) => {
  const {
    icon,
    type = "button",
    children = "",
    onClick,
    className = "",
    isDisabled = false,
    isLoaderOn = false,
    testID,
    accessibilityLabel,
    title,
    ref,
  } = props;

  const buttonClasses = type === "icon" ? "button-as-icon" : "button";

  const renderIcon = () => (
    <div className="button-icon-container">
      {isLoaderOn ? (
        <Loader />
      ) : (
        icon && <RenderLazyIcon icon={icon} fallback={<Loader />} />
      )}
    </div>
  );

  return (
    <button
      ref={ref}
      className={`${buttonClasses} ${className}`}
      onClick={onClick}
      disabled={isLoaderOn || isDisabled}
      type={type === "icon" ? "button" : type}
      style={{ cursor: isLoaderOn ? "progress" : "pointer" }}
      data-testid={testID}
      aria-label={accessibilityLabel}
      title={title}
    >
      {(type === "icon" || icon) && renderIcon()}
      {type !== "icon" && <label>{children}</label>}
    </button>
  );
};

export default Button;
