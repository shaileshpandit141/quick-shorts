import React from 'react';
import './RootLayout.css';
import { Outlet } from 'react-router-dom';
import { ToastContainer } from 'components';

const RootLayout: React.FC = () => {
  return (
    <>
      <ToastContainer />
      <Outlet />
    </>
  )
}

export default RootLayout;
