import React from 'react';
import './ButtonLink.css';
import { Link } from 'react-router-dom';
import { ButtonLinkProps } from './ButtonLink.types';
import { LazyIconImport } from 'lazyUtils/LazyIconImport/LazyIconImport';

const ButtonLink: React.FC<ButtonLinkProps> = (props) => {
  const {
    to,
    type,
    icon,
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
      {icon && (
        <span className='icon'>
          <LazyIconImport icon={icon} />
        </span>
      )}
      {children && (
        <span className='label'>{children}</span>
      )}
    </Link>
  )
}

export default ButtonLink;
