import React, { useState } from 'react'
import './GeminiChat.css'

function GeminiChat() {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      content: '¡Hola! 👋 Soy tu asistente nutricional IA powered by Gemini. Puedo ayudarte con información sobre 20 alimentos saludables. ¿En qué puedo ayudarte hoy?'
    }
  ])
  const [inputMessage, setInputMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const toggleChat = () => {
    setIsOpen(!isOpen)
  }

  const sendMessage = async () => {
    if (!inputMessage.trim() || isLoading) return

    const userMessage = { type: 'user', content: inputMessage }
    setMessages(prev => [...prev, userMessage])
    setInputMessage('')
    setIsLoading(true)

    try {
      const response = await fetch('http://localhost:5001/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mensaje: inputMessage })
      })

      const data = await response.json()
      
      if (data.success) {
        const botMessage = { type: 'bot', content: data.respuesta }
        setMessages(prev => [...prev, botMessage])
      } else {
        const errorMessage = { type: 'bot', content: 'Lo siento, hubo un error procesando tu consulta. 😔' }
        setMessages(prev => [...prev, errorMessage])
      }
    } catch (error) {
      const errorMessage = { type: 'bot', content: 'Error de conexión. Por favor, intenta de nuevo. 🔄' }
      setMessages(prev => [...prev, errorMessage])
    }

    setIsLoading(false)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      sendMessage()
    }
  }

  return (
    <>
      {/* Botón flotante */}
      <button 
        className={`gemini-chat-button ${isOpen ? 'active' : ''}`}
        onClick={toggleChat}
      >
        {isOpen ? '✕' : '🤖'}
      </button>

      {/* Modal del chat */}
      {isOpen && (
        <div className="gemini-chat-modal">
          <div className="gemini-chat-header">
            🤖 Asistente Nutricional IA
          </div>
          
          <div className="gemini-chat-messages">
            {messages.map((msg, index) => (
              <div key={index} className={`gemini-message ${msg.type}`}>
                {msg.content.split('\n').map((line, i) => (
                  <div key={i}>{line}</div>
                ))}
              </div>
            ))}
            
            {isLoading && (
              <div className="gemini-typing-indicator">
                <div className="gemini-typing-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
              </div>
            )}
          </div>

          <div className="gemini-chat-input-container">
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Pregunta sobre nutrición..."
              className="gemini-chat-input"
              disabled={isLoading}
            />
            <button
              onClick={sendMessage}
              disabled={!inputMessage.trim() || isLoading}
              className="gemini-send-button"
            >
              ➤
            </button>
          </div>
        </div>
      )}
    </>
  )
}

export default GeminiChat
