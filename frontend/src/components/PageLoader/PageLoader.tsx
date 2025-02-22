import React from 'react';
import './PageLoader.css';
import { Loader } from "components";
import { CircularProgress } from '@mui/material';

const PageLoader: React.FC = () => {
  return (
    <div className='loader'>
      <div className='icon-container'>
        <Loader />
      </div>
    </div>
  )
}

export default PageLoader
