import React from 'react';
import './Button.css';
import { LazyIcon } from 'lazyUtils/LazyIcon/LazyIcon';
import { LazyIconMapType } from 'lazyUtils/LazyIcon/LazyIcon.types';
import Loader from 'components/Loader/Loader';


interface ButtonProps {
  iconName?: keyof LazyIconMapType;
  label?: string;
  type: "button" | "submit";
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  className?: string;
  isDisabled?: boolean;
  isLoaderOn?: boolean;
}

const Button: React.FC<ButtonProps> = (props) => {
  const {
    iconName,
    label,
    type,
    onClick,
    className = '',
    isDisabled = false,
    isLoaderOn = false
  } = props;

  return (
    <button
      className={`${(iconName && !label) ? 'button-as-icon' : 'button'} ${className}`}
      onClick={onClick}
      disabled={isLoaderOn || isDisabled}
      type={type}
    >
      {iconName && (
        <div className='button-icon-container'>
          {(iconName && isLoaderOn)
            ? <Loader />
            : (
              <LazyIcon iconName={iconName} fallback={<Loader />} />
            )
          }
        </div>
      )}
      {label && (
        <label>{label}</label>
      )}
    </button>
  )
}

export default Button;
