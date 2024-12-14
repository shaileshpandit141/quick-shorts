import React from 'react'
import './DisplayErrors.css'

interface DisplayErrorsProps {
  message: string | string[]
}

const DisplayErrors: React.FC<DisplayErrorsProps> = (props) => {
  
  const { message } = props

  if (typeof message === 'string') {
    return (
      <p className='error-text'>{message}</p>
    )
  } else if (Array.isArray(message)) {
    return (
      message.map((msg, index) => (
        <p className='error-text' key={index}>{msg}</p>
      ))
    )
  } else {
    throw new Error('message prop only supported string and array of stying type')
  }
}

export default DisplayErrors
