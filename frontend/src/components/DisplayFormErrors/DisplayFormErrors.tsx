import React from 'react';
import './DisplayFormErrors.css';
import { Errors } from 'FeatureTypes';

interface DisplayFormErrorsProps {
  field: string;
  errors: Errors[];
}

const DisplayFormErrors: React.FC<DisplayFormErrorsProps> = ({ field, errors }) => {
  const renderErrors = () => (
    errors
      .filter(error => error.field === field)
      .map((error, index) => (
        <p className='error-message' key={index}>{error.message}</p>
      ))
  );

  const errorsJSX = renderErrors();

  if (errorsJSX.length === 0) {
    return null;
  }

  return (
    <div className='display-form-errors'>
      {errorsJSX}
    </div>
  );
};

export default DisplayFormErrors;
