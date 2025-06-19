import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import FloatingChat from './FloatingChat.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <FloatingChat />
  </StrictMode>,
)
