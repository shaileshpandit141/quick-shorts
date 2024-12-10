import React from 'react'
import './Loader.css'
import { CircularProgress } from '@mui/material';

const Loader: React.FC = () => {
  return (
    <div className='loader'>
      <div className='icon-container'>
        <CircularProgress
          color="primary"
          variant="indeterminate"
        />
      </div>
    </div>
  )
}

export default Loader
