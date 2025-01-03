import React, { useState, useEffect } from 'react'
import './ToggleThemeButton.css'
import { Button } from 'components'

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

  const handleToggleTheme = () => {
    setTheme(prevState => (
      prevState === 'light' ? 'dark' : 'light'
    ))
  }

  return (
    <Button
      iconName={theme === 'light' ? 'lightModeIcon' : 'darkModeIcon'}
      onClick={handleToggleTheme}
      className='toggle-theme-button'
    />
  )
}

export default ToggleThemeButton
