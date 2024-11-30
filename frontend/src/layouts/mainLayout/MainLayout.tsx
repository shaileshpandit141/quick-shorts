import React from 'react'
import './MainLayout.css'
import { Outlet } from 'react-router-dom'
import Header from 'componsnts/common/header/Header'
import Footer from 'componsnts/common/footer/Footer'

const MainLayout: React.FC = (props) => {
  return (
    <>
      <header className='inner-grid-1-1 grid-12'>
        <Header />
      </header>
      <main className='inner-grid-1-1 grid-12'>
        <Outlet />
      </main>
      <footer className='inner-grid-1-1 grid-12'>
        <Footer />
      </footer>
    </>
  )
}

export default MainLayout
