import React from 'react'
import './PageLoader.css'
import { CircularProgress } from '@mui/material';

const PageLoader: React.FC = () => {
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

export default PageLoader
