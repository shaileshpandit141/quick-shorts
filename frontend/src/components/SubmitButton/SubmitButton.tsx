import React from 'react'
import './SubmitButton.css'
import IconsMapType from 'lazyUtils/LazyIconImport/LazyIconImport.types'
import { LazyIconImport } from 'lazyUtils/LazyIconImport/LazyIconImport'
import Loader from '../Loader/Loader'

interface SubmitButtonProps {
  children: string;
  icon: keyof IconsMapType;
  isLoaderOn: boolean;
  isDisabled?: boolean;
  className?: string;
}

const SubmitButton: React.FC<SubmitButtonProps> = (props) => {
  const { children, icon, isLoaderOn, isDisabled = false, className } = props
  return (
    <button
      className={`button ${className}`}
      disabled={isLoaderOn || isDisabled}
    >
      <span className='icon'>
        {
          isLoaderOn
            ? <Loader />
            : <LazyIconImport icon={icon} />
        }
      </span>
      <span className='label'>{children}</span>
    </button>
  )
}

export default SubmitButton
