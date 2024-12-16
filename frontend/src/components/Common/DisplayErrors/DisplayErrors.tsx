import React from 'react'
import './DisplayErrors.css'

interface DisplayErrorsProps {
  message: string | string[]
}

const DisplayErrors: React.FC<DisplayErrorsProps> = (props) => {

  const { message } = props

  if (typeof message === 'string') {
    return (
      <div className='error-message-continer'>
        <p className='error-text-message'>{message}</p>
      </div>
    )
  } else if (Array.isArray(message)) {
    return (
      <div className='error-message-continer'>
        {
          message.map((msg, index) => (
            <p className='error-text-message' key={index}>{msg}</p>
          ))
        }
      </div>
    )
  } else {
    throw new Error('message prop only supported string and array of stying type')
  }
}

export default DisplayErrors
