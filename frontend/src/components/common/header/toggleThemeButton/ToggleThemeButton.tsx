import React, { useState, useEffect } from 'react'
import './ToggleThemeButton.css'
import { LazyIconImport } from 'lazyUtils/lazyIconImport'

type Theme = 'light' | 'dark'

const ToggleThemeButton: React.FC = () => {

  const [theme, setTheme] = useState<Theme>(() => {
    const savedTheme = localStorage.getItem('theme') as Theme
    return savedTheme || 'light'
  })

  useEffect(() => {
    const currentTheme = document.documentElement.getAttribute('data-theme')
    if (currentTheme !== theme) {
      document.documentElement.setAttribute('data-theme', theme)
      localStorage.setItem('theme', theme)
    }
  }, [theme])


  const Icon = () => (
    theme === 'light' ? <LazyIconImport icon='lightModeIcon' /> : <LazyIconImport icon='darkModeIcon' />
  )

  const handleToggleTheme = () => {
    setTheme(prevState => (
      prevState === 'light' ? 'dark' : 'light'
    ))
  }

  return (
    <button
      className='button button-as-icon'
      onClick={handleToggleTheme}
    >
      <span className='icon'>
        <Icon />
      </span>
    </button>
  )
}

export default ToggleThemeButton
