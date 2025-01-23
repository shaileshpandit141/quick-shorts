import React from 'react';
import './Button.css';
import { LazyIcon } from 'lazyUtils/LazyIcon/LazyIcon';
import { LazyIconMapType } from 'lazyUtils/LazyIcon/LazyIcon.types';
import Loader from 'components/Loader/Loader';


interface ButtonProps {
  type?: "button" | "submit" | "reset" | "icon";
  iconName?: keyof LazyIconMapType;
  children?: string | React.ReactNode;
  onClick?: React.MouseEventHandler<HTMLButtonElement>;
  className?: string;
  isDisabled?: boolean;
  isLoaderOn?: boolean;
}

const Button: React.FC<ButtonProps> = (props) => {
  const {
    iconName,
    type='button',
    children='',
    onClick,
    className='',
    isDisabled=false,
    isLoaderOn=false
  } = props;

  const buttonClasses = type === 'icon' ? 'button-as-icon' : 'button';

  const renderIcon = () => (
    <div className='button-icon-container'>
      {isLoaderOn ? (
        <Loader />
      ) : (
        iconName && <LazyIcon iconName={iconName} fallback={<Loader />} />
      )}
    </div>
  );

  return (
    <button
      className={`${buttonClasses} ${className}`}
      onClick={onClick}
      disabled={isLoaderOn || isDisabled}
      type={type === 'icon' ? 'button' : type}
      style={{cursor: isLoaderOn ? 'progress' : 'pointer'}}
    >
      {(type === 'icon' || iconName) && renderIcon()}
      {type !== 'icon' && children}
    </button>
  )
}

export default Button;
