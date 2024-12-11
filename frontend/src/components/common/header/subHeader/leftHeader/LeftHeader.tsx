import React from 'react'
import { Link } from 'react-router-dom'
import './LeftHeader.css'
import AppLogo from 'components/common/appLogo/AppLogo'

const LeftHeader: React.FC = (props) => {
  return (
    <div className='left-header'>
      <Link to='/' className='left-header-link'>
        <AppLogo />
        <h4>React</h4>
      </Link>
    </div>
  )
}

export default LeftHeader
