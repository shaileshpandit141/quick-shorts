import React from 'react'
import './IndexPage.css'
import { isAuthenticated } from 'features/auth'
import { Navigate } from 'react-router-dom'

const IndexPageSkeleton: React.FC = () => {
  if (isAuthenticated()) {
    return <Navigate to={'/home'} />
  }

  return (
    <div className='inner-grid-1-1 grid-12 index'>
      <div className="inner-grid-2-2 index-page">
        {/* Metadata settings */}
        <figure className="logo-container">
          <span className='img-skeleton skeleton'></span>
        </figure>
        <div className='heading-skeleton'>
          <span className='skeleton'></span>
          <span className='skeleton'></span>
        </div>
        <p className='paragraph-skeleton'>
          <span className='skeleton'></span>
          <span className='skeleton'></span>
        </p>
        <div className="buttons-skeleton">
          <span className='skeleton'></span>
          <span className='skeleton'></span>
        </div>
      </div>
    </div>
  )
}

export default IndexPageSkeleton
