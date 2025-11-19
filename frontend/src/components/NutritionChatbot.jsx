import React, { useState } from 'react'
import { sendChatMessage } from '../services/api'

function NutritionChatbot() {
  const [message, setMessage] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const handleSendMessage = async () => {
    if (!message.trim()) return

    const userMessage = { type: 'user', content: message }
    setMessages(prev => [...prev, userMessage])
    setMessage('')
    setLoading(true)

    try {
      const response = await sendChatMessage(message)
      const botMessage = { type: 'bot', content: response.response }
      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      const errorMessage = { type: 'bot', content: 'Error al procesar el mensaje' }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleSendMessage()
    }
  }

  return (
    <div className="chatbot-section">
      <h2>Chatbot Nutricional</h2>
      
      <div className="messages-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            <div className="message-content">
              {msg.content.split('\n').map((line, i) => (
                <div key={i}>{line}</div>
              ))}
            </div>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <div className="message-content">Escribiendo...</div>
          </div>
        )}
      </div>

      <div className="input-container">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Pregunta sobre información nutricional..."
          className="message-input"
        />
        <button
          onClick={handleSendMessage}
          disabled={!message.trim() || loading}
          className="send-button"
        >
          Enviar
        </button>
      </div>
    </div>
  )
}

export default NutritionChatbot
