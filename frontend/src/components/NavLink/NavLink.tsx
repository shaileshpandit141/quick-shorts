import React from "react";
import "./NavLink.css";
import { NavLink as Link } from "react-router-dom";
import './NavLink.css';
import { LazyIcon } from 'lazyUtils/LazyIcon/LazyIcon';
import { LazyIconMapType } from 'lazyUtils/LazyIcon/LazyIcon.types';
import Loader from 'components/Loader/Loader';

interface NavLinkProps {
  type: "link" | "icon";
  to: string;
  iconName?: keyof LazyIconMapType;
  children?: string | React.ReactNode;
  className?: string;
  isDisabled?: boolean;
  isLoaderOn?: boolean;
  testID?: string;
  accessibilityLabel?: string;
  title?: string;
  ref?: React.RefObject<HTMLAnchorElement>;
  target?: "_self" | "_blank" | "_parent" | "_top";
  isActive?: boolean;
}

const NavLink: React.FC<NavLinkProps> = (props) => {
  const {
    type = 'link',
    to,
    iconName,
    children = '',
    className = '',
    isDisabled = false,
    isLoaderOn = false,
    testID,
    accessibilityLabel,
    title,
    ref,
    target,
  } = props;

  const linkClasses = type === 'icon' ? 'link-as-icon' : 'link';
  const linkIsActive = ({ isActive }: { isActive: boolean }) => {
    return isActive ? "active" : "";
  }

  const renderIcon = () => (
    <div className='link-icon-container'>
      {isLoaderOn ? (
        <Loader />
      ) : (
        iconName && <LazyIcon iconName={iconName} fallback={<Loader />} />
      )}
    </div>
  );

  return (
    <Link
      ref={ref}
      to={isDisabled ? '#' : to}
      className={`${linkClasses} ${linkIsActive} ${className}`}
      style={{ cursor: isLoaderOn ? 'progress' : 'pointer' }}
      data-testid={testID}
      aria-label={accessibilityLabel}
      title={title}
      target={target}
    >
      {(type === 'icon' || iconName) && renderIcon()}
      {type !== 'icon' && <label>{children}</label>}
    </Link>
  )
};

export default NavLink;
