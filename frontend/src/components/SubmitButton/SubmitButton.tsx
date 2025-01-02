import React from 'react'
import './SubmitButton.css'
import { LazyIconMapType } from 'lazyUtils/LazyIcon/LazyIcon.types'
import { LazyIcon } from 'lazyUtils/LazyIcon/LazyIcon'
import Loader from '../Loader/Loader'

interface SubmitButtonProps {
  children: string;
  icon: keyof LazyIconMapType;
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
            : <LazyIcon iconName={icon} />
        }
      </span>
      <span className='label'>{children}</span>
    </button>
  )
}

export default SubmitButton
