import React, { useState, ChangeEvent } from 'react';
import './Input.css';
import { LazyIconImport } from 'lazyUtils/lazyIconImport';

interface InputProps {
  name: string;
  type: 'text' | 'password' | 'email' | 'number' | 'checkbox';
  value: string | number;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
  isRequired?: boolean;
  placeholder?: string; // Optional placeholder
}

const Input: React.FC<InputProps> = ({
  name,
  type,
  value,
  onChange,
  isRequired = false
}) => {
  const [isPasswordShow, setIsPasswordShow] = useState<boolean>(false);

  const handlePasswordShowButtonClick = (): void => {
    setIsPasswordShow((prevState) => !prevState);
  };

  return (
    <div className='input-component'>
      <div className='input-element-wrapper'>
        <div className='input-element'>
          <input
            name={name}
            type={type === 'password' ? (isPasswordShow ? 'text' : 'password') : type}
            id={name + type}
            value={value}
            onChange={onChange}
            required={isRequired}
            className='input'
            placeholder=''
            autoComplete="off"
          />
          <label htmlFor={name + type} className='label'>
            <span>{name}</span>
          </label>
        </div>
        {type === 'password' && (
          <div className='show-password-icon-container'>
            <button
              className='button button-as-icon'
              onClick={handlePasswordShowButtonClick}
              aria-label={isPasswordShow ? 'Hide password' : 'Show password'}
            >
              <span className='icon'>
                {isPasswordShow ? <LazyIconImport icon='eyeOpen' /> : <LazyIconImport icon='eyeClose' />}
              </span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default Input;
