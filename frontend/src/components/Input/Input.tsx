import React, { useState, ChangeEvent } from 'react';
import './Input.css';
import Button from 'components/Button/Button';
import DisplayFormErrors from '../DisplayFormErrors/DisplayFormErrors';
import { Errors } from 'FeatureTypes';

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
  onChange: (event: ChangeEvent<HTMLInputElement>) => void;
  readOnly?: boolean;
  errors?: Errors[]
  isRequired?: boolean;
  isDisabled?: boolean;
}

const Input: React.FC<InputProps> = ({
  name,
  type,
  value,
  onChange,
  isRequired = true,
  isDisabled = false,
  readOnly = false,
  errors = []
}) => {
  const [isPasswordShow, setIsPasswordShow] = useState(false);
  const id = name + type;
  const formattedLabel = name.split('_').join(' ');

  const commonInputProps = {
    name,
    type,
    id,
    onChange,
    required: isRequired,
    disabled: isDisabled,
    readOnly,
    className: 'input'
  };

  if (type === 'checkbox') {
    return (
      <div className='input-checkbox-component'>
        <div className='input-element-wrapper'>
          <div className='input-element'>
            <input
              {...commonInputProps}
              checked={Boolean(value)}
            />
            <label htmlFor={id} className='label'>
              <span>{formattedLabel}</span>
            </label>
          </div>
        </div>
        <DisplayFormErrors field={name} errors={errors} />
      </div>
    )
  }

  return (
    <div className='input-component'>
      <div className='input-element-wrapper'>
        <div className='input-element'>
          <input
            {...commonInputProps}
            type={type === 'password' ? (isPasswordShow ? 'text' : 'password') : type}
            value={typeof value !== 'boolean' ? value : String(value)}
            placeholder=''
            autoComplete="off"
          />
          <label htmlFor={id} className='label'>
            <span>{formattedLabel}</span>
          </label>
        </div>
        {type === 'password' && (
          <div className='show-password-icon-container'>
            <Button
              type='button'
              className='password-show-hide-button'
              iconName={isPasswordShow ? "eyeOpen" : "eyeClose"}
              onClick={() => setIsPasswordShow(prev => !prev)}
            />
          </div>
        )}
      </div>
      <DisplayFormErrors field={name} errors={errors} />
    </div>
  );
};

export default Input;
