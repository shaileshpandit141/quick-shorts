import React from 'react';
import './AnchorLink.css';
import { Link } from 'react-router-dom';
import { ButtonLinkProps } from './ButtonLink.types';
import { LazyIcon } from 'lazyUtils/LazyIcon/LazyIcon';

const AnchorLink: React.FC<ButtonLinkProps> = (props) => {
  const {
    to,
    type,
    iconName,
    className = '',
    children
  } = props

  return (
    <Link
      to={to}
      className={
        type === 'link'
          ? `link ${className}`
          : `link link-as-icon ${className}`
      }
    >
      {iconName && (
        <span className='icon'>
          <LazyIcon iconName={iconName} />
        </span>
      )}
      {children && (
        <span className='label'>{children}</span>
      )}
    </Link>
  )
}

export default AnchorLink;
