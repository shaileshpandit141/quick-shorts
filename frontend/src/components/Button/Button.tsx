import React from 'react';
import './Button.css';
import { ButtonProps } from './Button.types'
import { LazyIconImport } from 'lazyUtils/LazyIconImport/LazyIconImport';

const Button: React.FC<ButtonProps> = (props) => {
  const { type, icon, className = '', children, onClick } = props

  return (
    <button
      className={
        type === 'button'
          ? `button ${className}`
          : `button button-as-icon ${className}`
      }
      onClick={onClick}
    >
      {icon && (
        <span className='icon'>
          <LazyIconImport icon={icon} />
        </span>
      )}
      {children && (
        <span className='label'>{children}</span>
      )}
    </button>
  )
}

export default Button;
