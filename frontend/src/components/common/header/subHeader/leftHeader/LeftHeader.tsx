import React from 'react'
import { Link } from 'react-router-dom'
import './LeftHeader.css'

const LeftHeader: React.FC = (props) => {
  return (
    <div className='left-header'>
      <Link to='/' className='left-header-link'>
        <figure className='logo-container'>
          <img src='logo512.png' alt='logo-image' />
        </figure>
        <h4>React</h4>
      </Link>
    </div>
  )
}

export default LeftHeader
