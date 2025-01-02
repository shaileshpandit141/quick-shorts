import React from 'react';
import './Button.css';
import { ButtonProps } from './Button.types'
import { LazyIcon } from 'lazyUtils/LazyIcon/LazyIcon';

const Button: React.FC<ButtonProps> = (props) => {
  const { type, iconName, className = '', children, onClick } = props

  return (
    <button
      className={
        type === 'button'
          ? `button ${className}`
          : `button button-as-icon ${className}`
      }
      onClick={onClick}
    >
      {iconName && (
        <span className='icon'>
          <LazyIcon iconName={iconName} />
        </span>
      )}
      {children && (
        <span className='label'>{children}</span>
      )}
    </button>
  )
}

export default Button;
