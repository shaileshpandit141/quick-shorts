import React, { useState, ChangeEvent } from 'react';
import './Input.css';
import { LazyIcon } from 'lazyUtils/LazyIcon/LazyIcon';
import DisplayErrors from '../DisplayErrors/DisplayErrors';

interface InputProps {
  name: string;
  type: (
    'text'
    | 'password'
    | 'email'
    | 'url'
    | 'search'
    | 'tel'
    | 'number'
    | 'date'
    | 'datetime-local'
    | 'month'
    | 'week'
    | 'time'
    | 'checkbox'
  );
  value: string | number | boolean;
  onChange: (e: ChangeEvent<HTMLInputElement>) => void;
  isRequired?: boolean;
  isDisabled?: boolean;
  readOnly?: boolean;
  errorMessage?: string | string[]
}

const Input: React.FC<InputProps> = ({
  name,
  type,
  value,
  onChange,
  isRequired = true,
  isDisabled = false,
  readOnly = false,
  errorMessage = undefined
}) => {
  const [isPasswordShow, setIsPasswordShow] = useState<boolean>(false);

  const handlePasswordShowButtonClick = (): void => {
    setIsPasswordShow((prevState) => !prevState);
  };

  if (type === 'checkbox') {
    return (
      <div className='input-checkbox-component'>
        <div className='input-element-wrapper'>
          <div className='input-element'>
            <input
              name={name}
              type={type}
              id={name + type}
              checked={value === true ? true : false}
              onChange={onChange}
              required={isRequired}
              disabled={isDisabled}
              readOnly={readOnly}
              className='input'
            />
            <label htmlFor={name + type} className='label'>
              <span>{name.split('_').join(' ')}</span>
            </label>
          </div>
        </div>
        {
          errorMessage && (
            <DisplayErrors message={errorMessage} />
          )
        }
      </div>
    )
  }

  return (
    <div className='input-component'>
      <div className='input-element-wrapper'>
        <div className='input-element'>
          <input
            name={name}
            type={type === 'password' ? (isPasswordShow ? 'text' : 'password') : type}
            id={name + type}
            value={typeof value !== 'boolean' ? value : String(value)}
            onChange={onChange}
            required={isRequired}
            disabled={isDisabled}
            readOnly={readOnly}
            className='input'
            placeholder=''
            autoComplete="off"
          />
          <label htmlFor={name + type} className='label'>
            <span>{name.split('_').join(' ')}</span>
          </label>
        </div>
        {type === 'password' && (
          <div className='show-password-icon-container'>
            <button
              className='button button-as-icon'
              onClick={handlePasswordShowButtonClick}
              aria-label={isPasswordShow ? 'Hide password' : 'Show password'}
              type='button'
            >
              <span className='icon'>
                {isPasswordShow ? <LazyIcon iconName='eyeOpen' /> : <LazyIcon iconName='eyeClose' />}
              </span>
            </button>
          </div>
        )}
      </div>
      {
        errorMessage && (
          <DisplayErrors message={errorMessage} />
        )
      }
    </div>
  );
};

export default Input;
