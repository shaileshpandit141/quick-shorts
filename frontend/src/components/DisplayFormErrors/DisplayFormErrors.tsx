import React from 'react'
import './DisplayFormErrors.css'
import { Errors } from 'FeatureTypes';

interface DisplayFormErrorsProps {
  field: string
  errors: Errors[]
}

const DisplayFormErrors: React.FC<DisplayFormErrorsProps> = (props) => {
  const { field, errors } = props
  const renderErrors = () => (
    errors && errors.map((error, index) => (
      error.field === field && (
        <p className='error-message' key={index}>{error.message}</p>
      )
    ))
  );

  const errorsJSX = renderErrors();
  if (errorsJSX.length === 0) {
    return null;
  }

  return (
    <div className='display-form-errors'>
      {renderErrors()}
    </div>
  )
}

export default DisplayFormErrors;
